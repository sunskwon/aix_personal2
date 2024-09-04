import cv2

def ext_diff(imageA, imageB):
    
    grayA = cv2.cvtColor(imageA, cv2.COLOR_RGB2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_RGB2GRAY)
    
    diff = cv2.bitwise_xor(grayA, grayB)
    
    rev_diff = cv2.bitwise_not(diff)
    rev_diff = cv2.cvtColor(rev_diff, cv2.COLOR_GRAY2BGR)
    
    return rev_diff