from diffusers import DiffusionPipeline
import torch
import threading

pipe_lock = threading.Lock()

pipe = DiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16
)
pipe.to("cuda")
pipe.enable_attention_slicing()
pipe.enable_sequential_cpu_offload()

def generate_image(prompt: str, negative_prompt: str = "", steps: int = 7):
    with pipe_lock:
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            num_images_per_prompt=1
        ).images[0]
    return image
