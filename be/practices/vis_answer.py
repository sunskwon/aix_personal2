import torch
from datasets import load_dataset
from PIL import Image
from transformers import ViltProcessor, ViltForQuestionAnswering, pipeline

# Load dataset
dataset = load_dataset("Graphcore/vqa", split="validation[:200]", trust_remote_code=True)

# Choose an example
example = dataset[0]
image_id = example['image_id']
question = example['question']

# Load the image (assuming image_id is a file path; adjust if it's a URL)
image = Image.open(image_id)

# Initialize the processor and model
model_checkpoint = "dandelin/vilt-b32-mlm"
processor = ViltProcessor.from_pretrained(model_checkpoint)
model = ViltForQuestionAnswering.from_pretrained(model_checkpoint)

# Prepare inputs for the model
inputs = processor(images=image, text=question, return_tensors="pt")

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
inputs = {k: v.to(device) for k, v in inputs.items()}

# Forward pass
with torch.no_grad():
    outputs = model(**inputs)

# Get the predicted answer
logits = outputs.logits
idx = logits.argmax(-1).item()
answer = model.config.id2label[idx]

print("Question:", question)
print("Predicted answer:", answer)
