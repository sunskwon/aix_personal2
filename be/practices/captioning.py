from PIL import Image
import requests
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load the image
url = "https://huggingface.co/datasets/sayakpaul/sample-datasets/resolve/main/pokemon.png"
# image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
image = Image.open("./images/clock.png")

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Prepare the image and generate a caption
inputs = processor(images=image, return_tensors="pt").to(device)
outputs = model.generate(**inputs)

# Decode the generated caption
caption = processor.decode(outputs[0], skip_special_tokens=True)
print(caption)
