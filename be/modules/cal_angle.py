import cv2
import numpy as np

def detect_arrow_direction(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    height, width = gray.shape
    center = (width // 2, height // 2)

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(image, (x,y), (x + w, y + h), (0, 255, 0), 2)
        print(f"x: {x}, y: {y}, w: {w}, h: {h}")
        
        print(f"h / w: {h / w}")
        
        if h / w > 1.7:
            print("vertical")
            if abs(y + h - 225) < abs(y - 225):
                arrow_tip = (x + w // 2, y)
                start_point = (x + w // 2, y + h)
            else:
                arrow_tip = (x + w // 2, y + h)
                start_point = (x + w // 2, y)
        elif h / w < 0.2:
            print("lateral")
            if abs(x + w - 255) < abs(x - 225):
                arrow_tip = (x, y + h // 2)
                start_point = (x + w, y + h // 2)
            else:
                arrow_tip = (x + w, y + h // 2)
                start_point = (x, y + h // 2)
        else:                
            if abs(x + w - 225) < abs(x - 225):
                if abs(y + h - 225) < abs(y - 225):
                    print("2")
                    arrow_tip = (x, y)
                    start_point = (x + w, y + h)
                else:
                    print("3")
                    arrow_tip = (x, y + h)
                    start_point = (x + w, y)
            else:
                if abs(y + h - 225) < abs(y - 225):
                    print("1")
                    arrow_tip = (x + w, y)
                    start_point = (x, y + h)
                else:
                    print("4")
                    arrow_tip = (x + w, y + h)
                    start_point = (x, y)
            
        direction_vector = np.array(arrow_tip) - np.array(start_point)
        angle = np.arctan2(direction_vector[1], direction_vector[0]) * (180 / np.pi)
        angle = (angle + 360) % 360  # 0-360도 범위로 조정

        # print(f"화살표 방향: {angle:.2f}도")

        cv2.line(image, start_point, tuple(arrow_tip), (0, 255, 0), 2)
        cv2.circle(image, start_point, 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(arrow_tip), 5, (255, 0, 0), -1)

    # cv2.imshow('Arrow Direction', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return angle