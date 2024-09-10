from io import BytesIO
from ollama import generate
from PIL import Image

prompt = """
당신은 그림에 대해 설명해주는 도우미입니다.
그림에 적힌 숫자를 알려주세요.
대답은 숫자로만 해야하며, 숫자가 없다면 '0'이라고 응답하세요.
Don't narrate the answer, just answer the question.
Let's think step-by-step.
"""

def recog_num(image):
    
    pil_img = Image.fromarray(image)
    
    with BytesIO() as buffer:
        pil_img.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        
    full_response = ''
    
    for response in generate(
        model='llava:latest',
        prompt = prompt,
        images=[image_bytes],
        stream=True
    ):
        print(response['response'], end = '', flush = True)
        full_response += response['response']
        
    return full_response