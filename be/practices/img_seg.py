from transformers import pipeline
from PIL import Image
import requests
import cv2
import numpy as np

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/segmentation_input.jpg"
image = Image.open(requests.get(url, stream=True).raw)
# response = requests.get(url, stream=True).raw
# image_pil = Image.open(response).convert("RGB")

# # Convert PIL Image to NumPy array
# image_np = np.array(image_pil)

# # Convert RGB to BGR (OpenCV uses BGR)
# image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

# # Display image with OpenCV
# cv2.imshow("Image", image_cv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

semantic_segmentation = pipeline("image-segmentation", "nvidia/segformer-b1-finetuned-cityscapes-1024-1024")
results = semantic_segmentation(image)
for result in results:
    print(result)
    
    # Retrieve the mask (usually it's an image in PIL format)
    mask_pil = result["mask"]
    mask_np = np.array(mask_pil)
    
    # Ensure the mask is in grayscale (0-255) format
    if len(mask_np.shape) == 3:  # Convert RGB mask to grayscale if necessary
        mask_gray = cv2.cvtColor(mask_np, cv2.COLOR_RGB2GRAY)
    else:
        mask_gray = mask_np
    
    # Display the mask using OpenCV
    cv2.imshow("Segmentation Mask", mask_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()