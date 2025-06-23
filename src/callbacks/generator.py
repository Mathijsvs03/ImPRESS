import threading
from io import BytesIO
import uuid

import torch
import dash
from dash import Input, Output, callback, State, ALL, ctx
from diffusers import StableDiffusionPipeline
from src import utils, config

# Lock for thread-safe generation
pipe_lock = threading.Lock()
device = utils.get_device()

# Load pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to(device)


@callback(
    Output("history-store", "data"),
    Output("selected-image", "data", allow_duplicate=True),
    Output("selected-prompt", "children", allow_duplicate=True),
    State("Prompt", "value"),
    State("history-store", "data"),
    Input("generate-image-button", "n_clicks"),
    Input({'type': 'thumb', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def generate_image_from_prompt(prompt: str, history: list, n_clicks: int, thumb_clicks: list):
    triggered_id = ctx.triggered_id

    if isinstance(triggered_id, dict) and triggered_id.get("type") == "thumb":
        print('Image thumbnail clicked, updating selected image')
        clicked_id = triggered_id["index"]
        selected = next((item for item in reversed(history) if item["id"] == clicked_id), None)
        if selected is None:
            return dash.no_update, dash.no_update, dash.no_update
        return dash.no_update, selected["src"], selected["prompt"]

    if not prompt:
        print('No prompt provided, skipping image generation')
        return dash.no_update, dash.no_update, dash.no_update

    print('Waiting to acquire lock on model to generate image')
    steps = 50 

    with pipe_lock:
        image = pipe(
            prompt=prompt,
            num_inference_steps=steps,
            num_images_per_prompt=1
        ).images[0]

    image = image.resize(config.GENERATED_IMAGE_SIZE)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    source = utils.encode_image_to_base64(buffer.getvalue())

    new_entry = {
        "id": str(uuid.uuid4()),
        "src": source,
        "prompt": prompt
    }
    history.append(new_entry)

    return history, source, prompt
