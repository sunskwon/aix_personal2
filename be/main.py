import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from modules import cal_angle, cal_circ, ext_img_diff, recg_num, sep_num
from PIL import Image
from typing import Dict, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def cal_circularity(image):
    
    result = cal_circ.det_shape(image)
    
    return result

def eval_num(imageA, imageB):
    
    diff = ext_img_diff.ext_diff(imageA, imageB)
    
    sep_imgs = sep_num.preprocess(diff)

    numbers = []

    for i in range(len(sep_imgs)):
        
        result = recg_num.recog_num(sep_imgs[i])
        numbers.append(result)
        
    numbers = sorted(numbers)
        
    return numbers

def det_arrow(imageA, imageB):
    
    diff = ext_img_diff.ext_diff(imageA, imageB)
    
    angle = cal_angle.detect_arrow_direction(diff)
    
    return angle

@app.post("/uploadfile")
async def upload_file(files: List[UploadFile] = File(...)):
    
    images = []
    
    for file in files:
        
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        open_cv_image = np.asarray(image)
        images.append(open_cv_image)
    
    circularity = cal_circularity(images[0])
    number_list = eval_num(images[0], images[1])
    hour_angle = det_arrow(images[1], images[2])
    minute_angle = det_arrow(images[2], images[3])
    
    return {
        "circularity": circularity,
        "number": number_list,
        "hour_angle": hour_angle,
        "minute_angle": minute_angle,
    }
    
# import cv2

# imageA = cv2.imread('./images/step1.png')
# imageB = cv2.imread('./images/step2.png')
# imageC = cv2.imread('./images/step3.png')
# imageD = cv2.imread('./images/step4.png')

# circularity = cal_circularity(imageA)
# print(f"circularity: {circularity}")

# number = eval_num(imageA, imageB)
# print(f"number: {number}")

# hour_angle = det_arrow(imageB, imageC)
# print(f"hour_angle: {hour_angle}")

# minute_angle = det_arrow(imageC, imageD)
# print(f"minute_angle: {minute_angle}")