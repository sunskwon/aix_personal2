import tensorflow as tf

model = tf.keras.models.load_model('my_mnist_model.keras')

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

tf.random.set_seed(1234)

x_train, x_test = x_train / 255.0, x_test / 255.0

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

result = model.evaluate(x_test, y_test)
print("최종 예측 성공률(%): ", result[1]*100)