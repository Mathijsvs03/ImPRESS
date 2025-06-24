import threading
from io import BytesIO
import uuid

import torch
import dash
from dash import Input, Output, State, ALL, ctx, callback, html
from diffusers import StableDiffusionPipeline

from src import utils, config
from src.widgets.generated_panel import build_image_download_button

# 1) Lock and device setup
pipe_lock = threading.Lock()
device    = utils.get_device()
pipe      = StableDiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to(device)

@callback(
    Output("history-store",    "data"),
    Output("selected-image",   "data",      allow_duplicate=True),
    Output("selected-prompt",  "children",  allow_duplicate=True),
    Output("scatterplot",      "figure",    allow_duplicate=True),
    Output("generated-content","children"),
    State("Prompt",            "value"),
    State("history-store",     "data"),
    State("scatterplot",       "figure"),
    Input("generate-image-button",  "n_clicks"),
    Input({"type":"thumb","index":ALL}, "n_clicks"),
    prevent_initial_call=True
)
def generate_image_from_prompt(prompt, history, figure, gen_clicks, thumb_clicks):
    triggered = ctx.triggered_id

    # — 1) Thumbnail click: switch to that image —
    if isinstance(triggered, dict) and triggered.get("type") == "thumb":
        clicked_id = triggered["index"]
        sel = next((item for item in reversed(history) if item["id"] == clicked_id), None)
        if not sel:
            # nothing to update
            return (dash.no_update,)*5
        img = build_image_download_button(sel["src"])
        return dash.no_update, sel, sel["prompt"], dash.no_update, img

    # — 2) Empty prompt? do nothing —
    if not prompt or not prompt.strip():
        return (dash.no_update,)*5

    # — 3) Generate under lock —
    with pipe_lock:
        result = pipe(
            prompt=prompt,
            num_inference_steps=50,
            num_images_per_prompt=1
        )
        image = result.images[0]

    # — 4) Resize & encode to base64 —
    image = image.resize(config.GENERATED_IMAGE_SIZE)
    buf = BytesIO()
    image.save(buf, format="PNG")
    src64 = utils.encode_image_to_base64(buf.getvalue())

    # — 5) Project the new point —
    proj = utils.project_data_point(
        image_data={"path": buf, "image": image},
        prompt_data=prompt
    )
    x, y = proj["umap_x"], proj["umap_y"]
    figure["data"][0]["x"].append(x)
    figure["data"][0]["y"].append(y)
    figure["data"][0]["customdata"].append(src64)
    # if you’re using text for hover:
    if "text" in figure["data"][0]:
        figure["data"][0]["text"].append(prompt)

    # — 6) Add to history —
    entry = {
        "src":               src64,
        "prompt":            prompt,
        "projection_coords": proj,
        "id":                str(uuid.uuid4())
    }
    history.append(entry)

    # — 7) Build the <img> for display —
    gen_img = build_image_download_button(src64)

    # — 8) Return all outputs —
    return history, entry, prompt, figure, gen_img
