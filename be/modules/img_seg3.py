from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import requests

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

preprocessor = AutoImageProcessor.from_pretrained("google/deeplabv3_mobilenet_v2_1.0_513")
model = AutoModelForSemanticSegmentation.from_pretrained("google/deeplabv3_mobilenet_v2_1.0_513")

inputs = preprocessor(images=image, return_tensors="pt")

outputs = model(**inputs)
predicted_mask = preprocessor.post_process_semantic_segmentation(outputs)

print(outputs)
print(predicted_mask)