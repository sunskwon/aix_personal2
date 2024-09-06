import cv2
import numpy as np

def cls_shape(contour):
    
    # 윤곽선의 주변 추출
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    if len(approx) > 6:

        return True
    else:
        
        return False

def cal_ratio(contour):
    
    ellipse = cv2.fitEllipse(contour)
    (center, (MA, ma), angle) = ellipse
    
    # 장축과 단축의 비율 계산
    aspect_ratio = ma / MA
    
    return aspect_ratio

def cal_circularity(contour):
    
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    
    if perimeter == 0:
        return 0
    
    circularity = (4 * np.pi * area) / (perimeter **2)
    
    return circularity

def cal_score(scores):
    
    sum = 0
    
    for score in scores:
        sum += score
        
    ave = sum / len(scores)
    print(ave)
    
    if ave >= 0.8:
        return 1.0
    elif ave > 0.3:
        return 0.5
    else:
        return 0.0
    
def det_shape(image):
    
    # 이미지 흑백으로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 가장자리 검출
    edges = cv2.Canny(gray, 50, 150)
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    scores = []
    
    for contour in contours:
        # 다각형 여부 확인
        if cls_shape(contour):
            
            ratio = cal_ratio(contour)
            circularity = cal_circularity(contour)
            # print(f"ratio: {ratio}")
            # print(f"circularity: {circularity}")
            
            if circularity >= 0.8:
                scores.append(circularity / 0.8)
            elif circularity >= 0.2:
                if ratio > 1:
                    scores.append(circularity / (0.8 * ratio))
                else:
                    scores.append((circularity * ratio) / 0.8)
            else:
                if ratio > 1:
                    scores.append(0.5 / ratio)
                else:
                    scores.append(ratio / 2)
        else:
            scores.append(0)
            
    score = cal_score(scores)
    
    return score

if __name__ == "__main__":

    image = cv2.imread("./images/step1.png")
    print(det_shape(image))