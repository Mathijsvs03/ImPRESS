import threading
from io import BytesIO
from pathlib import Path

import uuid
import torch
import dash
from dash import Input, Output, callback, State, ALL, ctx
from diffusers import StableDiffusionPipeline
from src import utils, config

pipe_lock = threading.Lock()
device = utils.get_device()
pipe = StableDiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to(device)
# pipe.enable_attention_slicing()
# pipe.enable_sequential_cpu_offload()


@callback(
    Output("history-store", "data"),
    Output("selected-image", "data"),
    Output("scatterplot", "figure", allow_duplicate=True),
    State("Prompt", "value"),
    State("NegPrompt", "value"),
    State("history-store", "data"),
    State("scatterplot", "figure"),
    Input("generate-image-button", "n_clicks"),
    Input({'type': 'thumb', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)


def generate_image_from_prompt(prompt: str, negative_prompt: str, history: list, figure, n_clicks: int, thumb_clicks: list):
    triggered_id = ctx.triggered_id

    if isinstance(triggered_id, dict) and triggered_id.get("type") == "thumb":
        print('Image thumbnail clicked, updating selected image')
        index = triggered_id["index"]
        selected = list(reversed(history))[index]
        return dash.no_update, selected, dash.no_update

    if not prompt:
        print('No prompt provided, skipping image generation')
        return dash.no_update, dash.no_update, dash.no_update

    print('Waiting to acquire lock on model to generate image')
    steps = 50 # Can be adjusted to be controlled through UI (need to add in callback)
    with pipe_lock:
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            num_images_per_prompt=1
        ).images[0]

    # Resize and save the generated image
    image = image.resize(config.GENERATED_IMAGE_SIZE)
    image_path = Path(config.GENERATED_IMAGE_DIR) / f'gen_{uuid.uuid4().hex}.png'
    if not image_path.parent.exists():
        image_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(image_path)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    source = utils.encode_image_to_base64(buffer.getvalue())

    # Get projection coordinates for the generated image
    projection = utils.project_data_point(
        image_data={"path": buffer, "image": image},
        prompt_data=prompt
    )

    # Update the figure with the new image data
    x, y = projection['umap_x'], projection['umap_y']
    figure['data'][0]['x'].append(x)
    figure['data'][0]['y'].append(y)
    figure['data'][0]['customdata'].append(source)

    # Create the data entry for selected image
    data = {"src": source, "prompt": prompt, "projection_coords": projection}
    history.append(data)
    return history, data, figure
