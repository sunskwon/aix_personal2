import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# tf.random.set_seed(1234)

# x_train, x_test = x_train / 255.0, x_test / 255.0

# x_train = x_train.reshape(-1, 28, 28, 1)
# x_test = x_test.reshape(-1, 28, 28, 1)

# y_train = tf.keras.utils.to_categorical(y_train, 10)
# y_test = tf.keras.utils.to_categorical(y_test, 10)

model = tf.keras.models.load_model('my_mnist_model.keras')

# result = model.evaluate(x_test, y_test)
# print("최종 예측 성공률(%): ", result[1]*100)

import cv2
import numpy as np
import matplotlib.pyplot as plt

# img = cv2.imread('./images/num_example.png')
img = cv2.imread('./images/11.png')
plt.figure(figsize=(15,12))
print("img")

img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

ret, img_th = cv2.threshold(img_blur, 127, 255, cv2.THRESH_BINARY_INV)
contours, hierachy = cv2.findContours(img_th.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

rects = [cv2.boundingRect(each) for each in contours]

rects=sorted(rects)
thickness=abs(rects[0][2]-rects[1][2])*2

contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

cv2.drawContours(img_blur, biggest_contour, -1, (255, 255, 255), thickness)

ret, img_th = cv2.threshold(img_blur, 127, 255, cv2.THRESH_BINARY_INV)
contours, hierachy = cv2.findContours(img_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

rects = [cv2.boundingRect(each) for each in contours]
rects=sorted(rects)

img_for_class = img_blur.copy()

mnist_imgs=[]
margin_pixel = 15

for rect in rects:
    print(rect)
    im=img_for_class[rect[1]-margin_pixel:rect[1]+rect[3]+margin_pixel, rect[0]-margin_pixel:rect[0]+rect[2]+margin_pixel]
    row, col = im.shape[:2]
    
    bordersize=max(row, col)
    diff=min(row, col)
    
    bottom = im[row-2:row, 0:col]
    mean = cv2.mean(bottom)[0]
    
    border = cv2.copyMakeBorder(
        im,
        top=0,
        bottom=0,
        left=int((bordersize-diff)/2),
        right=int((bordersize-diff)/2),
        borderType=cv2.BORDER_CONSTANT,
        value=[mean, mean, mean]
    )
    
    square = border
    # cv2.imshow("image", square)
    # cv2.waitKey(0)
    
    resized_img=cv2.resize(square, dsize=(28,28), interpolation=cv2.INTER_AREA)
    mnist_imgs.append(resized_img)
    # cv2.imshow("image", resized_img)
    # cv2.waitKey(0)
    
for i in range(len(mnist_imgs)):
    
    img = mnist_imgs[i]
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    img=img.reshape(-1, 28, 28, 1)
    
    input_data = ((np.array(img) / 255) -1) * -1
    input_data
    
    res = np.argmax(model.predict(input_data), axis=-1)
    
    print(res)
# cv2.imshow("img", img_for_class)
# cv2.waitKey(0)