import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('my_mnist_model.keras')

img = cv2.imread('./images/57.png')
plt.figure(figsize=(15,12))

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

ret, img_th = cv2.threshold(img_blur, 127, 255, cv2.THRESH_BINARY_INV)
contours, hierachy = cv2.findContours(img_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

rects = [cv2.boundingRect(each) for each in contours]
rects = sorted(rects)

img_copy = img_blur.copy()

mnist_imgs = []
margin_pixel = 15

for rect in rects:
    print(rect)
    im=img_copy[rect[1]-margin_pixel:rect[1]+rect[3]+margin_pixel, rect[0]-margin_pixel:rect[0]+rect[2]+margin_pixel]
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
    
    resized_img = cv2.resize(square, dsize=(28, 28), interpolation=cv2.INTER_AREA)
    mnist_imgs.append(resized_img)
    # cv2.imshow("resized_img", resized_img)
    # cv2.waitKey(0)

for i in range(len(mnist_imgs)):
    
    img = mnist_imgs[i]
    cv2.imshow("img", img)
    cv2.waitKey(0)
    
    img = img.reshape(-1, 28, 28, 1)
    
    input_data = ((np.array(img) / 255) - 1) * -1
    
    res = np.argmax(model.predict(input_data), axis = -1)
    
    print(res)

# cv2.imshow("img", img_th)
# cv2.waitKey(0)