from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n-seg.pt")  # load an official model
# model = YOLO("path/to/best.pt")  # load a custom model

# Predict with the model
# results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
results = model("./images/dclock.png")

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