import torch
from diffusers import AutoPipelineForText2Image

pipeline = AutoPipelineForText2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")
meal = "Zucchini-Gnocchipfanne mit  vegetarischer Hacksauce"
prompt = "Pan of zucchini gnocchi with vegetarian mince sauce"
image = pipeline(
    prompt,
    guidance_scale=3.5,
    generator=torch.Generator("cpu").manual_seed(0),
).images[0]
image.save(f"meals/{meal}.png")
