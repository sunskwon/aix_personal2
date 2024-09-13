import cv2
import numpy as np
import os
from datetime import datetime
from fastapi import Depends, FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from modules import calculate_angle, calculate_circularity, extract_img_difference, separate_number
from modules import answer_rag, crawling_research
from modules import recognition_number
from PIL import Image
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def answering(query):
    
    try:
        answer = answer_rag.answer_rag(query)
        return answer
    except Exception as e:
        print(e)
        return ''

def cal_circularity(image):
    
    try:
        result = calculate_circularity.det_shape(image)
        return result
    except Exception as e:
        print(e)
        return 0.0

def det_arrow(imageA, imageB):
    
    try:
        diff = extract_img_difference.ext_diff(imageA, imageB)

        angle = calculate_angle.detect_arrow_direction(diff)
    
        return angle
    except Exception as e:
        print(e)
        return 0.0

def eval_num(imageA, imageB):
    
    try:
        diff = extract_img_difference.ext_diff(imageA, imageB)
    
        sep_imgs = separate_number.preprocess(diff)

        bool, numbers, num_infos = recognition_number.det_num(sep_imgs)
            
        return bool, numbers, num_infos
    except Exception as e:
        print(e)
        return False, [], []
    
def log_request_time(request: Request):
    start_time = datetime.now()
    request.state.start_time = start_time
    print(f"Request started at: {start_time}")
    yield
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Request ended at: {end_time}")
    print(f"Request duration: {duration}")

@app.get("/questiontest")
async def receive_question_test(query: str):
    
    return {
        "result": query,
    }
    
@app.post("/uploadtest")
async def upload_file_test(files: List[UploadFile] = File(...)):
    
    for file in files:
        
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        open_cv_image = np.asarray(image)
        cv2.imshow("image", open_cv_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
            
    return {
        "result": "hi",
    }

@app.get("/question", dependencies=[Depends(log_request_time)])
async def receive_question(query: str):
    
    answer = answering(query)
    
    return {
        "answer": answer
    }

@app.post("/uploadfile")
async def upload_file(files: List[UploadFile] = File(...)):
    
    images = []
    
    for file in files:
        
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        open_cv_image = np.asarray(image)
        images.append(open_cv_image)
    
    circularity = cal_circularity(images[0])
    bool_location, numbers, num_infos = eval_num(images[0], images[1])
    hour_angle = det_arrow(images[1], images[2])
    minute_angle = det_arrow(images[2], images[3])
    
    return {
        "circularity": circularity,
        "bool_location": bool_location,
        "numbers": numbers,
        "num_infos": num_infos,
        "hour_angle": hour_angle,
        "minute_angle": minute_angle,
    }

if __name__ == '__main__':

    import cv2

    # imageA = cv2.imread('./images/step1.png')
    # imageB = cv2.imread('./images/step2.png')
    # imageC = cv2.imread('./images/step3.png')
    # imageD = cv2.imread('./images/step4.png')

    # circularity = cal_circularity(imageA)
    # bool, numbers, num_infos = eval_num(imageA, imageB)
    # hour_angle = det_arrow(imageB, imageC)
    # minute_angle = det_arrow(imageC, imageD)
    
    # print(f"circularity: {circularity}")
    # print(f"bool: {bool}")
    # print(f"numbers: {numbers}")
    # print(f"hour_angle: {hour_angle}")
    # print(f"minute_angle: {minute_angle}")
    
    result = answering('벌레 물림 증상은?')
    print(result)