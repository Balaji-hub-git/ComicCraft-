import os
import re
import torch
from diffusers import StableDiffusionPipeline

device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "runwayml/stable-diffusion-v1-5"

# Load the pipeline once upon module load
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, 
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
pipe = pipe.to(device)

def sanitize_filename(prompt: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:25])
    return f"{cleaned}.png"

def generate_image(prompt: str, filename: str = None) -> str:
    """Generates a comic panel image based on the prompt and saves it locally."""
    if not filename:
        filename = sanitize_filename(prompt)
        
    image = pipe(prompt).images[0]
    output_path = os.path.join("static", "panels", filename)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return output_path