import threading
from io import BytesIO

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
    Output("selected-image", "data", allow_duplicate=True),
    State("Prompt", "value"),
    State("NegPrompt", "value"),
    State("history-store", "data"),
    Input("generate-image-button", "n_clicks"),
    Input({'type': 'thumb', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)


def generate_image_from_prompt(prompt: str, negative_prompt: str, history: list, n_clicks: int, thumb_clicks: list):
    triggered_id = ctx.triggered_id

    if isinstance(triggered_id, dict) and triggered_id.get("type") == "thumb":
        print('Image thumbnail clicked, updating selected image')
        index = triggered_id["index"]
        selected = list(reversed(history))[index]
        return dash.no_update, selected["src"]

    if not prompt:
        print('No prompt provided, skipping image generation')
        return dash.no_update, dash.no_update

    print('Waiting to acquire lock on model to generate image')
    steps = 50 # Can be adjusted to be controlled through UI (need to add in callback)
    with pipe_lock:
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            num_images_per_prompt=1
        ).images[0]

    image = image.resize(config.GENERATED_IMAGE_SIZE)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    source = utils.encode_image_to_base64(buffer.getvalue())

    history.append({"src": source, "prompt": prompt})
    return history, source
