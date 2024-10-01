import cv2
import numpy as np
import os
from datetime import datetime
from fastapi import Depends, FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from modules import cdt_analysis, cdt_llm_assist, cdt_preprocess
from modules import create_ocr_model
from modules import rag_generation
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

if not os.path.isfile("my_mnist_model.keras"):
    
    create_ocr_model.create_ocr_model()

def rag_answering(query):
    
    try:
        last_mark = query[len(query) - 1:]

        if last_mark != '?':
            query += '?'
        
        answer = rag_generation.rag_answer(query)
        answer = " ".join(answer.split())

        if any('\uAC00' <= char <= '\uD7A3' for char in answer):
            return answer
        else:
            return '{query}에 대한 정보를 찾을수 없습니다.'
        
    except Exception as e:
        
        print(e)
        return ''

def clock_drawing_test(img):

    try:
        img_crop = cdt_preprocess.crop_image(img)

        img_wo_circle, img_circle = cdt_preprocess.separate_circle(img_crop)
        cv2.imwrite('./images/temp_wo_circle.png', img_wo_circle)
        cv2.imwrite('./images/temp_circle.png', img_circle)

        img_sep_lst = cdt_preprocess.separate_numbers(img_wo_circle)

        img_hour, img_minute = cdt_preprocess.separate_needles(img_crop)

        circularity = cdt_analysis.cal_circularity(img_circle)

        numbers = []
        num_infos = []
        # count_nums = 0
        for img_sep in img_sep_lst:
            num = cdt_analysis.recog_number(img_sep['img'])
            # count_nums += 1
            if num >= 1 and num <= 12:
                numbers.append(num)
                num_infos.append({'num': num, 'rect': img_sep['rect']})
        numbers = set(numbers)
        llm_numbers = cdt_llm_assist.process_image(img_crop)
        llm_numbers = set(llm_numbers)

        diff_numbers = list(llm_numbers - numbers)
        numbers = list(llm_numbers | numbers)

        print(f"diff_numbers: {diff_numbers}")

        y_axis = next((item['rect'][1] for item in num_infos if item['num'] == 12), None)
        if y_axis == None:
            position = False
        else:
            for num_info in num_infos:
                if num_info['rect'][1] < y_axis:
                    position = False
                else:
                    position = True
        
        hour_angle = cdt_analysis.cal_arrow_angle(img_hour)
        minute_angle = cdt_analysis.cal_arrow_angle(img_minute)

        if hour_angle == None:
            if minute_angle == None:
                hour_angle = 370.0
                minute_angle = 370.0
            else:
                hour_angle = minute_angle
        elif minute_angle == None:
            minute_angle = hour_angle

        return circularity, numbers, position, hour_angle, minute_angle
    
    except Exception as e:
    
        print(e)
        return 0.0, [], False, 0.0, 0.0

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
async def upload_file_test(file: UploadFile = File(...)):
    
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
    
    answer = rag_answering(query)
    
    return {
        "answer": answer
    }

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    
    image_data = await file.read()
    image = Image.open(BytesIO(image_data))
    open_cv_image = np.asarray(image)
    open_cv_image = open_cv_image[:, :, :3]
    
    circularity, numbers, position, hour_angle, minute_angle = clock_drawing_test(open_cv_image)
    
    return {
        "circularity": circularity,
        "numbers": numbers,
        # "count_nums": count_nums,
        "bool_location": position,
        "hour_angle": hour_angle,
        "minute_angle": minute_angle,
    }

if __name__ == '__main__':

    import cv2

    for i in range(6):
        for j in range (1, 4):
            img_file = f"./images/{i}-{j}.png"
            
            img = cv2.imread(img_file)

            result = clock_drawing_test(img)
            print(f"{i}-{j}: {result}")

    img = cv2.imread('./images/clock.png')

    result = clock_drawing_test(img)
    print(result)

    # query = '안면마비 증상의 원인?'

    # result = rag_answering(query)
    # print(result)