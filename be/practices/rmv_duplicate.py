from PIL import Image
import numpy as np

def remove_duplicates(image1_path, image2_path, output_path):
    # 이미지 열기
    image1 = Image.open(image1_path).convert('RGB')
    image2 = Image.open(image2_path).convert('RGB')

    # 이미지 배열로 변환
    arr1 = np.array(image1)
    arr2 = np.array(image2)

    # 중복 부분을 찾기 위한 마스크 생성
    mask = (arr1 == arr2).all(axis=-1)
    
    # 중복 부분을 제거
    result_arr = np.where(mask[..., None], arr1, 0)
    
    # 결과 이미지를 저장
    result_image = Image.fromarray(result_arr)
    result_image.save(output_path)

# 사용 예
remove_duplicates('./images/clock_2.png', './images/clock.png', 'output.jpg')
