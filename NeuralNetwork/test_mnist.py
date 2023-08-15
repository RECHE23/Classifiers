from NeuralNetwork import NeuralNetwork
from NormalizationLayer import NormalizationLayer
from FullyConnectedLayer import FullyConnectedLayer
from ActivationLayer import ActivationLayer
from OutputLayer import OutputLayer
from activation_functions import tanh, sigmoid, relu, softmax
from loss_functions import mean_squared_error, categorical_cross_entropy
from keras.datasets import mnist
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score
import time

# load MNIST from server
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# training data : 60000 samples
# encode output which is a number in range [0,9] into a vector of size 10
# e.g. number 3 will become [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
y_train = to_categorical(y_train)

# same for test data : 10000 samples
#y_test = to_categorical(y_test)

# Network
net = NeuralNetwork()
net.add(NormalizationLayer())
net.add(FullyConnectedLayer(28*28, 100))
net.add(ActivationLayer(relu))
net.add(FullyConnectedLayer(100, 50))
net.add(ActivationLayer(relu))
net.add(FullyConnectedLayer(50, 33))
net.add(ActivationLayer(relu))
net.add(FullyConnectedLayer(33, 50))
net.add(ActivationLayer(relu))
net.add(FullyConnectedLayer(50, 10))
#net.add(OutputLayer(tanh, mean_squared_error))
net.add(OutputLayer(softmax, categorical_cross_entropy))

# Record start time:
start = time.time()

# Train:
net.fit(x_train[0:1000], y_train[0:1000], epochs=50, learning_rate=0.005, batch_size=5, shuffle=True)

# Test on N samples:
N = 10
out = net.predict(x_test[0:N], to="labels")
print("\n")
print("predicted values : ")
print(out, end="\n")
print("true values : ")
print(y_test[0:N])

# Record end time:
end = time.time()

# Print the difference between start and end time in milliseconds:
print("\nThe time of execution of above program is :", (end - start) * 10 ** 3, "ms")

y_predicted = net.predict(x_test, to="labels")
score = accuracy_score(y_test, y_predicted)
print(f"Accuracy score: {score:.2%}")
