import base64
import torch
import clip
import json
import io
import joblib
import numpy as np

from pathlib import Path
from PIL import Image
from datasets import DatasetDict, Value
from tqdm import tqdm
from umap import UMAP
from sklearn.manifold import TSNE
from src import config


_umap_model = None
_tsne_model = None

def get_device():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and torch.backends.mps.is_available():
        device = "mps"
    return device


def get_projector_models():
    global _umap_model, _tsne_model
    if _umap_model is None:
        u_path = Path(config.MODEL_DIR) / 'umap_model.pkl'
        if not u_path.exists():
            raise FileNotFoundError(f"UMAP model not found at {u_path}.")
        _umap_model = joblib.load(u_path)
    if _tsne_model is None:
        t_path = Path(config.MODEL_DIR) / 'tsne_model.pkl'
        if not t_path.exists():
            raise FileNotFoundError(f"t-SNE model not found at {t_path}.")
        _tsne_model = joblib.load(t_path)

    return _umap_model, _tsne_model


def decode_base64_to_image(base64_string):
    if not base64_string.startswith("data:image/png;base64,"):
        raise ValueError("Base64 string does not start with 'data:image/png;base64,'")
    base64_string = base64_string.replace("data:image/png;base64,", "")
    image_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_data)).convert("RGB")


def encode_image_to_base64(image):
    encoded_image = base64.b64encode(image).decode()
    return f"data:image/png;base64,{encoded_image}"


def image_to_base64_thumbnail(img, target_size=(64, 64)):
    img.thumbnail(target_size)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG", optimize=True)
    encoded = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"


def calculate_clip_embeddings(dataset):
    device = get_device()
    model, preprocess = clip.load("ViT-B/32", device=device)
    image_embeddings, prompt_embeddings, combined_embeddings = [], [], []

    for image, prompt in tqdm(zip(dataset['image'], dataset['prompt']), desc="Calculating CLIP embeddings"):
        image = Image.open(image['path']).convert("RGB") if isinstance(image, dict) else image
        image_input = preprocess(image).unsqueeze(0).to(device)
        text_input = clip.tokenize([prompt], truncate=True).to(device)
        with torch.no_grad():
            img_emb = model.encode_image(image_input).cpu().numpy()
            txt_emb = model.encode_text(text_input).cpu().numpy()
            comb_emb = (img_emb + txt_emb) / 2  # Average the embeddings

        image_embeddings.append(img_emb)
        prompt_embeddings.append(txt_emb)
        combined_embeddings.append(comb_emb)

    image_embeddings = np.concatenate(image_embeddings, axis=0)
    prompt_embeddings = np.concatenate(prompt_embeddings, axis=0)
    combined_embeddings = np.concatenate(combined_embeddings, axis=0)

    return combined_embeddings


def calculate_umap(clip_embeddings, n_components=2, n_neighbors=15, min_dist=0.1, metric='cosine'):
    umap_model = UMAP(n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, metric=metric)
    umap_embeddings = umap_model.fit_transform(clip_embeddings)
    path = Path(config.MODEL_DIR) / 'umap_model.pkl'
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(umap_model, path)
    umap_x, umap_y = umap_embeddings[:, 0], umap_embeddings[:, 1]
    return umap_x, umap_y


def calculate_tsne(clip_embeddings, n_components=2, perplexity=30, random_state=42):
    tsne_model = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state)
    tsne_embeddings = tsne_model.fit_transform(clip_embeddings)
    path = Path(config.MODEL_DIR) / 'tsne_model.pkl'
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(tsne_model, path)
    tsne_x, tsne_y = tsne_embeddings[:, 0], tsne_embeddings[:, 1]
    return tsne_x, tsne_y


def project_data_point(image_data, prompt_data):
    clip_emb = calculate_clip_embeddings({'image': [image_data], 'prompt': [prompt_data]})

    umap_model, tsne_model = get_projector_models()

    umap_embedding = umap_model.transform(clip_emb)
    umap_x, umap_y = umap_embedding[:, 0], umap_embedding[:, 1]
    umap_x, umap_y = umap_x.tolist(), umap_y.tolist()
    tsne_x, tsne_y = [None], [None] # t-SNE is not used in this function


    return {
        'umap_x': umap_x[0],
        'umap_y': umap_y[0],
        'tsne_x': tsne_x[0],
        'tsne_y': tsne_y[0],
    }


def generate_projections(dataset=None):
    if dataset is None:
        raise ValueError("Dataset could not be loaded. Please check the data source.")

    augmented_train = dataset['train']

    clip_embeddings = calculate_clip_embeddings(dataset['train'])
    print("Calculating UMAP projections...")
    umap_x, umap_y = calculate_umap(clip_embeddings)
    print("Calculating t-SNE projections...")
    tsne_x, tsne_y = calculate_tsne(clip_embeddings)

    image_paths = [item['image']['path'] for item in augmented_train]
    augmented_train = augmented_train.remove_columns("image")
    augmented_train = augmented_train.add_column("image", image_paths)
    augmented_train = augmented_train.cast_column("image", Value("string"))

    for col, val in zip(["umap_x", "umap_y", "tsne_x", "tsne_y"], [umap_x, umap_y, tsne_x, tsne_y]):
        if col in augmented_train.column_names:
            augmented_train = augmented_train.remove_columns(col)
        augmented_train = augmented_train.add_column(col, val)

    augmented_data = DatasetDict({"train": augmented_train})

    with open(config.RUNTIME_CONFIG_PATH) as f:
        augmented_path = json.load(f).get('AUGMENTED_DATASET_PATH', None)
        if not augmented_path:
            raise ValueError("AUGMENTED_DATASET_PATH not found in runtime config.")

    augmented_data.save_to_disk(augmented_path)
