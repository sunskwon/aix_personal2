from transformers import pipeline
from PIL import Image
import requests

# Load image
url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/segmentation_input.jpg"
image = Image.open(requests.get(url, stream=True).raw)

# Initialize semantic segmentation pipeline
segmentation = pipeline("image-segmentation", model="nvidia/segformer-b1-finetuned-cityscapes-1024-1024")

# Perform segmentation
results = segmentation(image)

# Process and display the segmentation masks
for result in results:
    mask = result["mask"]
    mask.show()  # Display the mask using PIL
