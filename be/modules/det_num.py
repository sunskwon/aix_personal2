import cv2
import img_diff
import numpy as np

def preprocess(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rev_gray = cv2.bitwise_not(gray)
    
    _, thresh = cv2.threshold(rev_gray, 50, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((6, 6), np.int8)
    dilation = cv2.dilate(thresh, kernel, iterations=2)
    
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    
    contours, hierachy = cv2.findContours(closing, cv2.RETR_EXTERNAL, 1)
    img_contour = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    
    for contour in contours:
        
        x, y, w, h = cv2.boundingRect(contour)
        img_crop = image.copy()[y:y + h, x:x + w]
        
        cv2.imshow("img_crop", img_crop)
        cv2.waitKey(0)
    
    return image

def det_num(image):
    
    return None

image = cv2.imread('./images/dnumbers.png')
result = preprocess(image)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()