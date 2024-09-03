import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

img_original = cv2.imread('./images/dnumandarrow.png')
# cv2.imshow("img_original", img_original)
# cv2.waitKey(0)

img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
# cv2.imshow("img_gray", img_gray)
# cv2.waitKey(0)

img_gray = cv2.bitwise_not(img_gray)
_, thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
# cv2.imshow("thresh", thresh)
# cv2.waitKey(0)

# adaptive_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
# cv2.imshow("adaptive_thresh", adaptive_thresh)
# cv2.waitKey(0)

kernel = np.ones((3, 3), np.int8)
dilation = cv2.dilate(thresh, kernel, iterations=1)
# cv2.imshow("dilation", dilation)
# cv2.waitKey(0)

closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
# cv2.imshow("closing", closing)
# cv2.waitKey(0)

contours, hierachy = cv2.findContours(closing, cv2.RETR_EXTERNAL, 1)

img_contour = cv2.drawContours(img_original, contours, -1, (0, 255, 0), 2)
# cv2.imshow("img_contour", img_contour)
# cv2.waitKey(0)

contour_pos = []
for pos in range(len(contours)):
    area = cv2.contourArea(contours[pos])
    if area > 100:
        contour_pos.append(pos)

for pos in contour_pos:
    x, y, w, h = cv2.boundingRect(contours[pos])
    img_crop = img_original[y:y + h, x:x + w]
    cv2.imshow("img_crop", img_crop)
    cv2.waitKey(0)

# for p in contour_pos:
#     img_temp = cv2.imread('./images/dnumandarrow.png')
#     img_orig = cv2.imread('./images/dnumandarrow.png')
#     x, y, w ,h = cv2.boundingRect(contours[p])
    
#     cnt = contours[p]
#     area = cv2.contourArea(cnt)
    
#     area_box = w*h
    
#     img_contour = cv2.drawContours(img_orig, contours, p, (0, 255, 0), 1)
    
#     cnt = contours[p]
#     M = cv2.moments(cnt)
#     cx = int(M['m10']/M['m00'])
#     cy = int(M['m01']/M['m00'])
    
#     for i in range(y, y + h):
#         px_lst = img_contour[i]
        
#         for j in range(x, x + w):
#             if (px_lst[j] == [0, 255, 0]).all():
#                 cv2.line(img_contour, (j, i), (cx, cy), (1, 2, 3), 2)
    
#     img_crop = img_contour[y:y + h, x:x + w]
    
#     for i in range(y, y + h):
#         px_lst = img_contour[i]
        
#         for j in range(x, x + w):
#             if (px_lst[j] != [1, 2, 3]).all():
#                 cv2.line(img_temp, (j, i), (j, i), (0, 0, 0), 2)
                
#     img_save = img_temp[y:y + h, x:x + w]
    
#     cv2.imshow("image", img_save)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()