import cv2

def ext_diff(imageA, imageB):
    
    grayA = cv2.cvtColor(imageA, cv2.COLOR_RGB2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_RGB2GRAY)
    
    diff = cv2.bitwise_xor(grayA, grayB)
    rev_diff = cv2.bitwise_not(diff)
    
    return rev_diff

imageA = cv2.imread('./images/dnumbers.png')
imageB = cv2.imread('./images/dnumandarrow.png')
diff = ext_diff(imageA, imageB)
# cv2.imshow("image", diff)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# diff_colored = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
# result = cv2.bitwise_and(imageA, diff_colored)
# cv2.imshow("origin", imageA)
# cv2.imshow("image", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()