import base64
import torch

def get_device():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and torch.backends.mps.is_available():
        device = "mps"
    return device


def encode_image_to_base64(image):
    encoded_image = base64.b64encode(image).decode()
    return f"data:image/png;base64,{encoded_image}"

