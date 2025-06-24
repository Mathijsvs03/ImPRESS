import threading
from io import BytesIO
import uuid

import torch
from dash import Input, Output, State, ALL, ctx, callback, html
from diffusers import StableDiffusionPipeline

from src import utils, config
from src.Dataset import Dataset

pipe_lock = threading.Lock()
device    = utils.get_device()
pipe      = StableDiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to(device)

@callback(
    Output("history-store",   "data"),
    Output("selected-image",  "data",        allow_duplicate=True),
    Output("selected-prompt", "children",    allow_duplicate=True),
    Output("scatterplot",     "figure",      allow_duplicate=True),
    Output("generated-content","children"),            
    State("Prompt",           "value"),
    State("history-store",    "data"),
    State("scatterplot",      "figure"),
    Input("generate-image-button", "n_clicks"),
    Input({"type":"thumb","index":ALL},    "n_clicks"),
    prevent_initial_call=True
)
def generate_image_from_prompt(prompt, history, figure, gen_clicks, thumb_clicks):
    triggered = ctx.triggered_id

    if isinstance(triggered, dict) and triggered.get("type") == "thumb":
        clicked_id = triggered["index"]
        sel = next((item for item in reversed(history) if item["id"] == clicked_id), None)
        if not sel:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        img = html.Img(src=sel["src"], className="gen-image", alt="Generated image")
        return dash.no_update, sel, sel["prompt"], dash.no_update, img


    if not prompt or not prompt.strip():
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    with pipe_lock:
        res   = pipe(prompt=prompt, num_inference_steps=50, num_images_per_prompt=1)
        image = res.images[0]

    image = image.resize(config.GENERATED_IMAGE_SIZE)
    buf   = BytesIO()
    image.save(buf, format="PNG")
    src64 = utils.encode_image_to_base64(buf.getvalue())


    proj = utils.project_data_point(
        image_data={"path": buf, "image": image},
        prompt_data=prompt
    )
    x, y = proj["umap_x"], proj["umap_y"]
    figure["data"][0]["x"].append(x)
    figure["data"][0]["y"].append(y)
    figure["data"][0]["customdata"].append(src64)


    entry = {
        "src":               src64,
        "prompt":            prompt,
        "projection_coords": proj,
        "id":                str(uuid.uuid4())
    }
    history.append(entry)

    gen_img = html.Img(src=src64, className="gen-image", alt="Generated image")

    return history, entry, prompt, figure, gen_img
