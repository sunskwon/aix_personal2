import cv2
import numpy as np

def classify_shape(contour):
    # 윤곽선의 주변을 추출
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    num_vertices = len(approx)
    if num_vertices == 4:
        # 사각형일 경우, 직사각형인지 확인하기 위해 각도를 계산
        angles = []
        for i in range(num_vertices):
            p1 = approx[i]
            p2 = approx[(i + 1) % num_vertices]
            p3 = approx[(i + 2) % num_vertices]
            
            # 벡터 생성
            v1 = p2 - p1
            v2 = p3 - p2
            
            # 벡터의 내적을 이용하여 각도 계산
            dot_product = np.dot(v1.flatten(), v2.flatten())
            mag_v1 = np.linalg.norm(v1)
            mag_v2 = np.linalg.norm(v2)
            angle = np.arccos(dot_product / (mag_v1 * mag_v2))
            
            angles.append(angle)
        
        # 모든 각도가 직각(90도)에 가까운지 확인
        if all(np.isclose(angle, np.pi / 2, atol=0.1) for angle in angles):
            return "Rectangle"
        else:
            return "Quadrilateral"
    else:
        # 타원의 특성을 가진 윤곽선인지 확인하기 위해 측정 (여기서는 간단히 'Ellipse'로 표시)
        return "Ellipse"

def detect_shapes(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 가장자리 검출
    edges = cv2.Canny(gray, 50, 150)
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        shape = classify_shape(contour)
        
        # 윤곽선에 맞는 사각형을 그리기
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

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