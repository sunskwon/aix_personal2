import cv2
import numpy as np
import separate_number, recognition_number, calculate_angle

def crop_image(image):

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, img_th = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(img_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # img_cont = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)

    x, y, w, h = cv2.boundingRect(contours[0])
    # print(f"x: {x}, y: {y}, w: {w}, h: {h}")
    margin = 10
    size = max(w, h)

    if w > h:
        diff = (w - h) // 2
        # print(diff)
        img_cropped = image[y - diff - margin:y + w - diff + margin, x - margin:x + w + margin]
    else:
        diff = (h - w) // 2
        # print(diff)
        img_cropped = image[y - margin:y + h + margin, x - diff - margin:x + h - diff + margin]

    # height, width, _ = img_cropped.shape
    # print(f"height: {height}, width: {width}")

    # img = cv2.cvtColor(img_cropped, cv2.COLOR_GRAY2BGR)
    # cv2.circle(img_cropped, ((size // 2) + margin, (size // 2) + margin), 3, (0, 0, 255), -1)

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
    img_no_circle = cv2.drawContours(image.copy(), biggest_contour, -1, (255, 255, 255), thickness)
    img_only_circle = cv2.drawContours(white_image, biggest_contour, -1, (0, 0, 0), 2)

    return [img_no_circle, img_only_circle]

def extract_needles(image):

    height, width, _ = image.shape
    radius = height // 4

    kernel = np.ones((5, 5), np.uint8)

    mask = np.ones(image.shape, dtype=np.uint8)
    cv2.circle(mask, (width // 2, height // 2), radius, (255, 255, 255), -1, cv2.LINE_AA)
    mask = cv2.dilate(mask, kernel, iterations=3)
    
    img_masked = cv2.bitwise_and(results[0], mask)
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

    img = cv2.imread('./images/clock.png')
    # img = cv2.imread('./images/cirle.png')
    # height, width, _ = img.shape
    # print(f"height: {height}, width: {width}")

    result = crop_image(img)
    # cv2.imshow('img', img)
    # cv2.imshow('result', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    results = separate_circle(result)
    # cv2.imshow('result1', results[0])
    # cv2.imshow('result2', results[1])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    masked_image = extract_needles(results[0])
    # height, width, _ = masked_image.shape
    # cv2.circle(masked_image, (width // 2, height // 2), height // 4, (0, 0, 255), 1, cv2.LINE_AA)
    # cv2.circle(masked_image, (width // 2, height // 2), height // 8, (0, 0, 255), 1, cv2.LINE_AA)
    # cv2.circle(masked_image, (width // 2, height // 2), height // 16, (0, 0, 255), 1, cv2.LINE_AA)

    # img_circle = cv2.circle(results[0], (width // 2, height // 2), 60, (0, 0, 0), -1, cv2.LINE_4)
    # cv2.circle(results[0], (width // 2, height // 2), 30, (0, 255, 0), 2, cv2.LINE_4)
    # cv2.circle(results[0], (width // 2, height // 2), 10, (0, 0, 255), 2, cv2.LINE_4)

    # minute = np.ones(masked_image.shape, dtype=np.uint8) * 255
    # hour = np.ones(masked_image.shape, dtype=np.uint8) * 255

    # ur_image = masked_image[:height // 2, width // 2:]
    # ul_image = masked_image[:height // 2, :width //2]
    # lr_image = masked_image[height // 2:, width // 2:]
    # ll_image = masked_image[height // 2:, :width // 2]

    # minute[:height // 2, width // 2:] = ur_image
    # hour[:height // 2, :width //2] = ul_image
    # cv2.imshow('img_circle', masked_image)
    # cv2.imshow('ur', ur_image)
    # cv2.imshow('ul', ul_image)
    # cv2.imshow('lr', lr_image)
    # cv2.imshow('ll', ll_image)

    hour, minute = separate_needles(masked_image)
    cv2.imshow('minute', minute)
    cv2.imshow('hour', hour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # sep_lst = separate_number.preprocess(img_circle)
    # for sep in sep_lst:
    #     cv2.imshow('result', sep['img'])
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # bool, numbers, num_infos = recognition_number.det_num(sep_lst)
    # print(numbers)

    hour_angle = calculate_angle.detect_arrow_direction(hour)
    minute_angle = calculate_angle.detect_arrow_direction(minute)

    print(f"hour: {hour_angle}, minute: {minute_angle}")
