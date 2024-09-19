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
    cv2.imshow('contour image', img_contour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    crop_imgs = []
    margin_pixel = 15
    
    for contour in contours:
        
        x, y, w, h = cv2.boundingRect(contour)
        
        img_crop = image.copy()[y:y + h, x:x + w]
        
        crop_h, crop_w = img_crop.shape[:2]
        white_background = np.ones((crop_h + 2 * margin_pixel, crop_w + 2 * margin_pixel, 3), dtype=np.uint8) * 255
        
        white_background[margin_pixel:margin_pixel + crop_h, margin_pixel:margin_pixel + crop_w] = img_crop
        
        crop_imgs.append({'img': white_background, 'rect': cv2.boundingRect(contour)})
        
    return crop_imgs

if __name__ == '__main__':
    
    image = cv2.imread('./images/numbers.png')
    
    results = preprocess(image)
    for result in results:
        print(result['rect'])
        cv2.imshow("image", result['img'])
        cv2.waitKey(0)
        cv2.destroyAllWindows()