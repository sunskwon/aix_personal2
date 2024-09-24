import cv2
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('my_mnist_model.keras')

def cal_circularity(img):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(img_gray, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # img_contour = cv2.drawContours(img.copy(), contours[0], -1, (0, 255, 0), 2)
    # cv2.drawContours(img_contour, contours[1], -1, (255, 0, 0), 2)
    # cv2.drawContours(img_contour, contours[4], -1, (0, 0, 255), 2)
    # cv2.imshow('img_contour', img_contour)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    scores = []
    
    for contour in contours:
        # print(f"area: {cv2.contourArea(contour)}")
        # img_contour = cv2.drawContours(img.copy(), contour, -1, (0, 255, 0), 2)
        # cv2.imshow('img_contour', img_contour)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if cv2.contourArea(contour) > 400:
            if len(contour) >= 5:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                _, (MA, ma), _ = cv2.fitEllipse(contour)
                aspect_ratio = ma / MA
                # print(f"aspect_ratio: {aspect_ratio}")

                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    circularity = 0
                else:
                    circularity = (4 * np.pi * area) / (perimeter**2)
                # print(f"circularity: {circularity}")
                if len(approx) > 6:
                    
                    if circularity >= 0.8:
                        scores.append(circularity / 0.8)
                    elif circularity >= 0.2:
                        if aspect_ratio > 1:
                            scores.append(circularity / (0.8 * aspect_ratio))
                        else:
                            scores.append((circularity * aspect_ratio) / 0.8)
                    else:
                        if aspect_ratio > 1:
                            scores.append(0.5 / aspect_ratio)
                        else:
                            scores.append(aspect_ratio / 2)
                else:
                    scores.append(0)
            else:
                scores.append(0)

        # print(f"area: {cv2.contourArea(contour)}, len(contour): {len(contour)}, aspect_ratio: {aspect_ratio}, circularity: {circularity}, len(approx): {len(approx)}, ")
    
    # print(scores)
    sum = 0

    for score in scores:
        sum += score
    
    if len(scores) > 0:
        ave = sum / len(scores)
    else:
        ave = 0.0

    if ave >= 0.8:
        return 1.0
    elif ave > 0.3:
        return 0.5
    else:
        return 0.0
    
def recog_number(img):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    
    _, img_threshold = cv2.threshold(img_blur, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rects = [cv2.boundingRect(each) for each in contours]
    rects = sorted(rects)
    
    cropped_imgs = []
    margin = 15
    
    for rect in rects:
        im = img_blur[rect[1] - margin:rect[1] + rect[3] + margin, rect[0] - margin:rect[0] + rect[2] + margin]
        row, col = im.shape[:2]
    
        bordersize = max(row, col)
        diff = min(row, col)
    
        bottom = im[row - 2:row, 0:col]
        mean = cv2.mean(bottom)[0]
    
        border = cv2.copyMakeBorder(
            im,
            top = 0,
            bottom = 0,
            left = int((bordersize - diff) / 2),
            right = int((bordersize - diff) / 2),
            borderType = cv2.BORDER_CONSTANT,
            value = [mean, mean, mean]
        )
        
        square = border
        
        img_resized = cv2.resize(square, dsize=(28, 28), interpolation=cv2.INTER_AREA)
        cropped_imgs.append(img_resized)
        
    number = 0
        
    for i in range(len(cropped_imgs)):
        
        img = cropped_imgs[i]
        img = img.reshape(-1, 28, 28, 1)
        
        input_data = ((np.array(img) / 255) - 1) * -1
        
        res = np.argmax(model.predict(input_data), axis = -1)
        
        if number == 0:
            number = int(res[0])
        else:
            number *= 10
            number += int(res[0])
        
    return number

# def recog_clock(img):

#     model = tf.keras.models.load_model('my_cdt_model.keras')

#     img_resized = cv2.resize(img, (100, 100))

#     img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

#     input_data = img_gray.reshape(1, 100, 100, 1) / 255.0

#     res = np.argmax(model.predict(input_data), axis = -1)
    
#     return res

def cal_arrow_angle(img):

    try:

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

        edges = cv2.Canny(img_blur, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        height, width = img_gray.shape
        if height // 2 == width // 2:
            center = height // 2
        else:
            center = max(height, width) // 2

        for contour in contours:
            
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(img, (x,y), (x + w, y + h), (0, 255, 0), 2)
            
            if h / w > 1.7:
                # print("vertical")
                if abs(y + h - center) < abs(y - center):
                    arrow_tip = (x + w // 2, y)
                    start_point = (x + w // 2, y + h)
                else:
                    arrow_tip = (x + w // 2, y + h)
                    start_point = (x + w // 2, y)
            elif h / w < 0.2:
                # print("lateral")
                if abs(x + w - center) < abs(x - center):
                    arrow_tip = (x, y + h // 2)
                    start_point = (x + w, y + h // 2)
                else:
                    arrow_tip = (x + w, y + h // 2)
                    start_point = (x, y + h // 2)
            else:                
                if abs(x + w - center) < abs(x - center):
                    if abs(y + h - center) < abs(y - center):
                        # print("2")
                        arrow_tip = (x, y)
                        start_point = (x + w, y + h)
                    else:
                        # print("3")
                        arrow_tip = (x, y + h)
                        start_point = (x + w, y)
                else:
                    if abs(y + h - center) < abs(y - center):
                        # print("1")
                        arrow_tip = (x + w, y)
                        start_point = (x, y + h)
                    else:
                        # print("4")
                        arrow_tip = (x + w, y + h)
                        start_point = (x, y)
                
            direction_vector = np.array(arrow_tip) - np.array(start_point)
            angle = np.arctan2(direction_vector[1], direction_vector[0]) * (180 / np.pi)
            angle = (angle + 450) % 360  # 0-360도 범위로 조정

        return angle
    
    except Exception as e:
        
        print(e)
        return None

if __name__ == '__main__':
    
    img = cv2.imread('./images/temp_circle.png')
    print(cal_circularity(img))

    # img = cv2.imread('./images/arrow.png')
    # print(recog_number(img))
    
    # img = cv2.imread('./images/arrow.png')
    # print(cal_arrow_angle(img))

    # for i in range(6):
    #     for j in range(1, 4):
    #         file_name = f"./images/{i}-{j}.png"
    #         img = cv2.imread(file_name)
    #         result = recog_clock(img)
    #         print(f"{i}-{j}.png : {result}")