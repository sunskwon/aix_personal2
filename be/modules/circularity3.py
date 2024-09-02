import cv2
import numpy as np

def calculate_circularity(contour):
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    
    if perimeter == 0:
        return 0
    
    circularity = (4 * np.pi * area) / (perimeter ** 2)
    return circularity

def detect_shapes(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 가장자리 검출
    edges = cv2.Canny(gray, 50, 150)
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        circularity = calculate_circularity(contour)
        print(f"{image_path}'s circularity: {circularity}")
        
        # 윤곽선에 맞는 사각형을 그리기
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f'Circularity: {circularity:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # 결과 이미지 표시
    cv2.imshow('Detected Shapes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 이미지 경로를 입력하여 함수 호출
detect_shapes('./images/sqare.png')
detect_shapes('./images/ellipse.png')
detect_shapes('./images/circle.png')
detect_shapes('./images/dcircle.png')
detect_shapes('./images/dellipse.png')