import numpy as np
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_data_from_directory(data_dir):
    images = []
    labels = []

    for label in range(6):
        label_dir = os.path.join(data_dir, str(label))
        for filename in os.listdir(label_dir):
            if filename.endswith('.png'):
                img_path = os.path.join(label_dir, filename)
                img = load_img(img_path, target_size=(100, 100), color_mode='grayscale')
                img = img_to_array(img) / 255.0  # 정규화
                images.append(img)
                labels.append(label)

    print(images)
    print(labels)

    return np.array(images), np.array(labels)

def create_cdt_model(data_dir):
    x_data, y_data = load_data_from_directory(data_dir)

    # 데이터를 훈련과 테스트로 분리 (80% 훈련, 20% 테스트)
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=1234)

    x_train = x_train.reshape(-1, 100, 100, 1)
    x_test = x_test.reshape(-1, 100, 100, 1)

    y_train = tf.keras.utils.to_categorical(y_train, 6)
    y_test = tf.keras.utils.to_categorical(y_test, 6)

    # 데이터 증강
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False,
        fill_mode='nearest'
    )

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(kernel_size=(3,3), filters=64, input_shape=(100,100,1), padding='same', activation='relu'),
        tf.keras.layers.Conv2D(kernel_size=(3,3), filters=64, padding='same', activation='relu'),
        tf.keras.layers.MaxPool2D(pool_size=(2,2)),
    
        tf.keras.layers.Conv2D(kernel_size=(3,3), filters=128, padding='same', activation='relu'),
        tf.keras.layers.Conv2D(kernel_size=(3,3), filters=256, padding='valid', activation='relu'),
        tf.keras.layers.MaxPool2D(pool_size=(2,2)),
        
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(units=256, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(units=6, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), metrics=['accuracy'])
    model.summary()

    # 모델 학습 (데이터 증강 사용)
    model.fit(datagen.flow(x_train, y_train, batch_size=1), 
              steps_per_epoch=len(x_train), 
              epochs=10, 
              validation_data=(x_test, y_test))

    # 테스트 데이터에 대한 평가
    result = model.evaluate(x_test, y_test)
    print("테스트 데이터 예측 성공률(%): ", result[1]*100)

    # 훈련 데이터에 대한 평가
    train_result = model.evaluate(x_train, y_train)
    print("훈련 데이터 예측 성공률(%): ", train_result[1]*100)

    # 모델 저장
    model.save('my_cdt_model.keras')

if __name__ == '__main__':
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dataset')
    create_cdt_model(root_dir)
