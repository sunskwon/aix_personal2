import cv2
from ollama import generate

prompt = """
You are the explainer who explains the image.
Please answer the Question based on the given image.

Question:
List all numbers in image.
Each items must be separated by a comma.
"""

def process_image(img):
    
    _, buffer = cv2.imencode('.png', img)

    image_bytes = buffer.tobytes()
    
    result = generate(
        model='bakllava:latest', 
        prompt=prompt, 
        images=[image_bytes],
    )

    answer = []

    if 'to' in result['response']:
        temp = result['response'].split()

        for i in range(int(temp[0]), int(temp[2]) + 1):
            if i > 0 and i < 13:
                answer.append(i)
    elif ',' not in result['response']:
        if ' ' not in result['response'] and int(result['response']) > 20:

            for c in str(result['response']):
                if int(c) > 0 and int(c) < 13:
                    answer.append(int(c))
        else:
            temp = result['response'].split()

            for item in temp:
                if int(item) > 0 and int(item) < 13:
                    answer.append(int(item))
    else:
        if ', ' in result['response']:
            temp = result['response'].split(', ')
        else:
            temp = result['response'].split(',')

        for item in temp:
            try:
                if int(item) > 0 and int(item) < 13:
                    answer.append(int(item))
            except Exception as e:
                print(e)
    
    return answer

if __name__ == '__main__':

    # for i in range(6):
    #     for j in range(1, 4):
            
    #         image_dir = f"./images/{i}-{j}.png"
            
    #         img = cv2.imread(image_dir)
            
    #         description = process_image(img)

    #         print(f"{i}-{j}: {description}")

    img = cv2.imread('./images/0-2.png')

    description = process_image(img)

    print(description)