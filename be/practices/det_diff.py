from skimage.metrics import structural_similarity as ssim
import argparse
import imutils
import cv2
from skimage import io

imageA = cv2.imread("./images/dnumbers.png")
imageB = cv2.imread("./images/dnumandarrow.png")
# cv2.imshow("imageA", imageA)
# cv2.waitKey(0)
# cv2.imshow("imageB", imageB)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

grayA = cv2.cvtColor(imageA, cv2.COLOR_RGB2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_RGB2GRAY)
# cv2.imshow("grayA", grayA)
# cv2.waitKey(0)
# cv2.imshow("grayB", grayB)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

score, diff = ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
# cv2.imshow("diff", diff)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# diff = cv2.bitwise_not(diff)
# cv2.imshow("diff", diff)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]
# cv2.imshow("thresh", thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    area = cv2.contourArea(c)
    if area > 30:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (51, 255, 102), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (51, 255, 102), 2)
        
# cv2.imshow('Original', imageA)
# cv2.imshow('Modified', imageB)
# cv2.imshow('CroppedA', imageA)
# cv2.imshow('CroppedB', imageB)
# cv2.waitKey(0)
# cv2.destroyAllWindows()