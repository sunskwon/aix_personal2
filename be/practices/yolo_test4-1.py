import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n-obb.pt")  # load an official model
# model = YOLO("path/to/best.pt")  # load a custom model

image = cv2.imread("./images/dclock.png")
image2 = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (5, 5), 0)
gray = cv2.bitwise_not(gray)

adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# cv2.imshow("image", adaptive_threshold)
# cv2.waitKey(0)
rev_adaptive_threshold = cv2.bitwise_not(adaptive_threshold)
# cv2.imshow("image", rev_adaptive_threshold)
# cv2.waitKey(0)
rev_adaptive_threshold = cv2.cvtColor(rev_adaptive_threshold, cv2.COLOR_GRAY2BGR)

# Predict with the model
# results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
results = model(rev_adaptive_threshold)

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
    # result.save(filename="result.jpg")  # save to disk