from diffusers import DiffusionPipeline
import torch
from huggingface_hub import login
login("")

pipe = DiffusionPipeline.from_pretrained(
  "CompVis/stable-diffusion-v1-4",
  torch_dtype=torch.float16
)
pipe.to("cuda")
pipe.enable_attention_slicing()
pipe.enable_sequential_cpu_offload()

prompt = "Astronaut in a space, photorealistic, detailed"
image = pipe(prompt).images[0]
image.save(f"{prompt}.png")