import cv2
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('my_mnist_model.keras')

def recog_num(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierachy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    rects = [cv2.boundingRect(each) for each in contours]
    rects = sorted(rects)
    
    mnist_imgs = []
    # margin_pixel = 15
    margin_pixel = 0
    
    for rect in rects:
        im = blur[rect[1] - margin_pixel:rect[1] + rect[3] + margin_pixel, rect[0] - margin_pixel:rect[0] + rect[2] + margin_pixel]
        row, col = im.shape[:2]
    
        bordersize = max(row, col)
        diff = min(row, col)
    
        # bottom = im[row - 2:row, 0:col]
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
        
        resized_img = cv2.resize(square, dsize=(28, 28), interpolation=cv2.INTER_AREA)
        mnist_imgs.append(resized_img)
        
    result = 0
        
    for i in range(len(mnist_imgs)):
        
        img = mnist_imgs[i]
        img = img.reshape(-1, 28, 28, 1)
        
        input_data = ((np.array(img) / 255) - 1) * -1
        
        res = np.argmax(model.predict(input_data), axis = -1)
        # print(f"res: {res}")
        
        if result == 0:
            result = int(res[0])
        else:
            result *= 10
            result += int(res[0])
        
    return result