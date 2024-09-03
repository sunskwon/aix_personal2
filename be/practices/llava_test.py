from ollama import generate
import glob
import pandas as pd
from PIL import Image
import os
from io import BytesIO

def process_image(image_file, prompt):
    print(f"\nProcessing {image_file}\n")
    with Image.open(image_file) as img:
        with BytesIO() as buffer:
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()

    full_response = ''
    # 이미지에 대한 설명 생성하기
    for response in generate(model='llava:latest', 
                             prompt=prompt, 
                             images=[image_bytes], 
                             stream=True):
        # 콘솔에 응답을 인쇄하고 전체 응답에 추가합니다.
        print(response['response'], end='', flush=True)
        full_response += response['response']
    
    return full_response

# Example usage
custom_prompt = """
당신은 그림에 대해 설명해주는 역할을 수행합니다.
주어진 그림에 대해 설명해주세요.
그림은 아날로그 시계를 사람이 그린 그림 입니다.
아날로그 시계는 테두리, 숫자, 시침과 분침으로 이루어져 있습니다.
각 요소에 대해 자세하되 간략하게 설명하세요.
한글로 대답하세요.
Don't narrate the answer, just answer the question.
Let's think step-by-step.
"""
description = process_image("./images/dclock.png", custom_prompt)
print("\nFinal Description:\n", description)
