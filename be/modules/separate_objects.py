import cv2
import numpy as np

def crop_image(image):

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, img_th = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(img_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y, w, h = cv2.boundingRect(contours[0])
    margin = 10

    if w > h:
        diff = (w - h) // 2
        img_cropped = image[y - diff - margin:y + w - diff + margin, x - margin:x + w + margin]
    else:
        diff = (h - w) // 2
        img_cropped = image[y - margin:y + h + margin, x - diff - margin:x + h - diff + margin]

    return img_cropped

def separate_circle(image):

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    
    _, img_th = cv2. threshold(img_blur, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(img_th.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    rects = [cv2.boundingRect(each) for each in contours]
    rects = sorted(rects)
    thickness = abs(rects[0][2] - rects[1][2]) * 2

    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key = lambda x : x[0])[1]
    
    white_image = np.ones(image.shape, dtype=np.uint8) * 255
    img_wo_circle = cv2.drawContours(image.copy(), biggest_contour, -1, (255, 255, 255), thickness)
    img_circle = cv2.bitwise_xor(img_wo_circle, image)
    img_circle = cv2.bitwise_not(img_circle)

    return img_wo_circle, img_circle

def extract_needles(image):

    height, width, _ = image.shape
    radius = height // 4

    kernel = np.ones((5, 5), np.uint8)

    mask = np.ones(image.shape, dtype=np.uint8)
    cv2.circle(mask, (width // 2, height // 2), radius, (255, 255, 255), -1, cv2.LINE_AA)
    mask = cv2.dilate(mask, kernel, iterations=3)
    
    img_masked = cv2.bitwise_and(image, mask)
    img_masked = cv2.bitwise_xor(img_masked, mask)
    img_masked = cv2.bitwise_not(img_masked)

    return img_masked

def separate_needles(image):

    height, width, _ = image.shape

    img_hour = np.ones(image.shape, dtype=np.uint8) * 255
    img_minute = np.ones(image.shape, dtype=np.uint8) * 255

    img_hour[:height // 2, :width //2] = image[:height // 2, :width //2]
    img_minute[:height // 2, width // 2:] = image[:height // 2, width // 2:]

    return img_hour, img_minute

if __name__ == '__main__':

    import calculate_angle, calculate_circularity, recognition_number, separate_number

    img = cv2.imread('./images/clock.png')

    img_crop = crop_image(img)
    # cv2.imshow('img_crop', img_crop)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    img_wo_circle, img_circle = separate_circle(img_crop)
    # cv2.imshow('img_wo_circle', img_wo_circle)
    # cv2.imshow('img_circle', img_circle)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    circularity = calculate_circularity.det_shape(img_circle)
    print(f"circularity: {circularity}")

    sep_lst = separate_number.preprocess(img_wo_circle)
    # for sep in sep_lst:
    #     cv2.imshow('result', sep['img'])
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    bool, numbers, num_infos = recognition_number.det_num(sep_lst)
    print(f"bool: {bool}, numbers: {numbers}")

    img_needles = extract_needles(img_wo_circle)
    hour, minute = separate_needles(img_needles)
    # cv2.imshow('minute', minute)
    # cv2.imshow('hour', hour)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    hour_angle = calculate_angle.detect_arrow_direction(hour)
    minute_angle = calculate_angle.detect_arrow_direction(minute)

    print(f"hour: {hour_angle}, minute: {minute_angle}")
