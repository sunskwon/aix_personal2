from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model(["./images/dnumbers.png", "./images/dclock.png"])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    print(f"boxes: {boxes}")
    masks = result.masks  # Masks object for segmentation masks outputs
    print(f"masks: {masks}")
    keypoints = result.keypoints  # Keypoints object for pose outputs
    print(f"keypoints: {keypoints}")
    probs = result.probs  # Probs object for classification outputs
    print(f"probs: {probs}")
    obb = result.obb  # Oriented boxes object for OBB outputs
    print(f"obb: {obb}")
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk