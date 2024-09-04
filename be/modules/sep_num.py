import cv2
import numpy as np

def preprocess(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rev_gray = cv2.bitwise_not(gray)
    
    _, thresh = cv2.threshold(rev_gray, 50, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((6, 6), np.int8)
    dilation = cv2.dilate(thresh, kernel, iterations=2)
    
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    
    contours, hierachy = cv2.findContours(closing, cv2.RETR_EXTERNAL, 1)
    img_contour = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)
    
    crop_imgs = []
    
    for contour in contours:
        
        x, y, w, h = cv2.boundingRect(contour)
        img_crop = image.copy()[y:y + h, x:x + w]
        crop_imgs.append(img_crop)
        
    return crop_imgs