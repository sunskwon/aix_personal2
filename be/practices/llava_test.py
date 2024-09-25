import cv2
from io import BytesIO
from ollama import generate
from PIL import Image
# import glob
# import pandas as pd
# import os

def process_image(image_file, prompt):
    print(f"\nProcessing {image_file}\n")
    with Image.open(image_file) as img:
        with BytesIO() as buffer:
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()

    # full_response = ''
    # # 이미지에 대한 설명 생성하기
    # for response in generate(model='bakllava:latest', 
    #                          prompt=prompt, 
    #                          images=[image_bytes], 
    #                          stream=True,):
    #     # 콘솔에 응답을 인쇄하고 전체 응답에 추가합니다.
    #     print(response['response'], end='', flush=True)
    #     full_response += response['response']
    
    result = generate(
        model='bakllava:latest', 
        prompt=prompt, 
        images=[image_bytes],
    )
    
    return result['response']

# Example usage
custom_prompt = """
당신은 그림에 대해 설명해주는 친절한 설명가입니다.
주어진 그림에 대해 설명해주세요.
한글로 설명하세요.

Question:
list all numbers in image
"""

for i in range(6):
    for j in range(1, 4):
        
        image_dir = f"./images/{i}-{j}.png"

        description = process_image(image_dir, custom_prompt)

        print(f"{i}-{j}: {description}")


# description1 = process_image('./images/4-3.png', custom_prompt)
# description2 = process_image('./images/temp_wo_circle.png', custom_prompt)

# print()
# print(description1)
# print(description2)