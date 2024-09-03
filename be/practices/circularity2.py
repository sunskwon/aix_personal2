import cv2
import numpy as np

def calculate_ellipse_aspect_ratio(contour):
    if len(contour) < 5:
        return None
    
    ellipse = cv2.fitEllipse(contour)
    (center, (MA, ma), angle) = ellipse
    
    # 장축과 단축의 비율 계산
    aspect_ratio = ma / MA
    
    return aspect_ratio

def detect_shapes(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 가장자리 검출
    edges = cv2.Canny(gray, 50, 150)
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        aspect_ratio = calculate_ellipse_aspect_ratio(contour)
        
        if aspect_ratio:
            # 타원의 축 비율을 시각적으로 표시
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, f'Aspect Ratio: {aspect_ratio:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # 결과 이미지 표시
    cv2.imshow('Detected Shapes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 이미지 경로를 입력하여 함수 호출
# detect_shapes('./images/sqare.png')
# detect_shapes('./images/ellipse.png')
# detect_shapes('./images/circle.png')
# detect_shapes('./images/dcircle.png')
# detect_shapes('./images/dellipse.png')
detect_shapes('./images/open_ellip.png')