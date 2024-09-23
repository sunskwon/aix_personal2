import cv2
import numpy as np

def crop_image(img):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_threshold = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('img_threshold', img_threshold)
    
    contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # img_contours = cv2.drawContours(img, contours[15], -1, (0, 255, 0), 2)
    # cv2.imshow('img_contours', img_contours)
    # for contour in contours:
    #     print(cv2.boundingRect(contour))

    rects = [cv2.boundingRect(each) for each in contours]
    rects = sorted(rects)
    # x, y, w, h = cv2.boundingRect(contours[0])
    x, y, w, h = rects[0]
    margin = 10

    if w > h:
        diff = (w - h) // 2
        img_cropped = img[y - diff - margin:y + w - diff + margin, x - margin:x + w + margin]
    else:
        diff = (h - w) // 2
        img_cropped = img[y - margin:y + h + margin, x - diff - margin:x + h - diff + margin]

    return img_cropped

def separate_circle(img):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    
    _, img_threshold = cv2. threshold(img_blur, 127, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(img_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # for contour in contours:
    #     print(f"area: {cv2.contourArea(contour)}")
    #     img_contours = cv2.drawContours(img.copy(), contour, -1, (0, 255, 0), 6)
    #     cv2.imshow('img_contours', img_contours)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    rects = [cv2.boundingRect(each) for each in contours]
    # print(rects)
    rects = sorted(rects)
    # print(rects)
    
    mag = 1.0

    thickness = int(abs(rects[0][2] - rects[1][2]) * mag)
    # print(f"thickness: {thickness}")
    if thickness > 100:
        rects_sorted = sorted(rects, key=lambda r: r[2], reverse=True)
        thickness = int(abs(rects_sorted[0][2] - rects_sorted[1][2]) * mag)
        if thickness > 100:
            thickness = 8
    # print(f"thickness: {thickness}")

    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key = lambda x : x[0])[1]
    
    img_wo_circle = cv2.drawContours(img.copy(), biggest_contour, -1, (255, 255, 255), thickness)
    # cv2.imshow('img_wo_circle', img_wo_circle)

    img_circle = cv2.bitwise_xor(img_wo_circle, img)
    img_circle = cv2.bitwise_not(img_circle)
    # img_circle = np.ones(img.shape, dtype=np.uint8) * 255
    # cv2.drawContours(img_circle, biggest_contour, -1, (0, 0, 0), thickness)

    return img_wo_circle, img_circle

def separate_numbers(img):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_rev_gray = cv2.bitwise_not(img_gray)
    
    _, img_threshold = cv2.threshold(img_rev_gray, 50, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((6, 6), np.int8)
    dilation = cv2.dilate(img_threshold, kernel, iterations=2)
    
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, 1)
    
    cropped_imgs = []
    margin = 15
    
    for contour in contours:
        
        x, y, w, h = cv2.boundingRect(contour)
        
        img_crop = img.copy()[y:y + h, x:x + w]
        
        crop_h, crop_w = img_crop.shape[:2]
        white_background = np.ones((crop_h + (2 * margin), crop_w + (2 * margin), 3), dtype=np.uint8) * 255
        white_background[margin:margin + crop_h, margin:margin + crop_w] = img_crop
        
        cropped_imgs.append({'img': white_background, 'rect': cv2.boundingRect(contour)})
        
    return cropped_imgs

def separate_needles(img):

    height, width, _ = img.shape
    radius = height // 5
    
    img_hour = np.ones(img.shape, dtype=np.uint8) * 255
    img_minute = np.ones(img.shape, dtype=np.uint8) * 255

    kernel = np.ones((5, 5), np.uint8)

    mask = np.ones(img.shape, dtype=np.uint8)
    cv2.circle(mask, (width // 2, height // 2), radius, (255, 255, 255), -1, cv2.LINE_AA)
    mask = cv2.dilate(mask, kernel, iterations=3)
    
    img_masked = cv2.bitwise_and(img, mask)
    img_masked = cv2.bitwise_xor(img_masked, mask)
    img_masked = cv2.bitwise_not(img_masked)

    img_hour[:height // 2, :width //2] = img_masked[:height // 2, :width //2]
    img_minute[:height // 2, width // 2:] = img_masked[:height // 2, width // 2:]

    return img_hour, img_minute

if __name__ == '__main__':

    img = cv2.imread('./images/4-1.png')
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img_crop = crop_image(img)
    height, width, _ = img_crop.shape
    cv2.imshow('img_crop', img_crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"height: {height}, width: {width}")
    
    img_wo_circle, img_circle = separate_circle(img_crop)
    cv2.imwrite('./modules/temp_circle.png', img_circle)
    cv2.imshow('img_wo_circle', img_wo_circle)
    cv2.imshow('img_circle', img_circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # sep_lst = separate_numbers(img_wo_circle)
    # for sep in sep_lst:
    #     cv2.imshow('result', sep['img'])
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # img_hour, img_minute = separate_needles(img_crop)
    # cv2.imshow('minute', img_minute)
    # cv2.imshow('hour', img_hour)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()