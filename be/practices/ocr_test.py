import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# 1. 데이터셋 로드 및 전처리
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 데이터 정규화 (0~255를 0~1로 변환)
x_train, x_test = x_train / 255.0, x_test / 255.0

# 2. 모델 정의
model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),       # 28x28 이미지를 1차원 배열로 변환
    layers.Dense(128, activation='relu'),        # 은닉층
    layers.Dense(10, activation='softmax')       # 출력층 (10개의 클래스로 분류)
])

# 3. 모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 4. 모델 학습
model.fit(x_train, y_train, epochs=5)

# 5. 모델 평가
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'\n테스트 정확도: {test_acc}')

# 6. 손글씨 이미지 파일을 읽어와서 추론하는 함수
def preprocess_image(image_path):
    # 이미지 열기
    img = Image.open(image_path).convert('L')  # 흑백으로 변환
    img = img.resize((28, 28))  # 모델 입력 크기로 리사이즈
    img_array = np.array(img)
    img_array = img_array / 255.0  # 정규화
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
    return img_array

def predict_digit(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_digit = np.argmax(predictions)
    return predicted_digit

# 7. 예시 이미지로 추론
image_path = './images/1.png'  # 사용자 이미지 경로
predicted_digit = predict_digit(image_path)
print(f'예측된 숫자: {predicted_digit}')

# 예측 결과 시각화
img = Image.open(image_path)
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap=plt.cm.gray_r)
plt.title("Input Image")

plt.subplot(1, 2, 2)
plt.bar(range(10), model.predict(preprocess_image(image_path))[0])
plt.title("Prediction Probabilities")
plt.xlabel("Digit")
plt.ylabel("Probability")
plt.xticks(range(10))

plt.show()