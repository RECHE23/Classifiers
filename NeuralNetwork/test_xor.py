import time
import numpy as np

from neural_network import NeuralNetwork
from layers import *
from functions import *


# Training data:
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([[0], [1], [1], [0]])

# Network:
net = NeuralNetwork()
net.add(FullyConnectedLayer(2, 3))
net.add(ActivationLayer(tanh))
net.add(FullyConnectedLayer(3, 1))
net.add(OutputLayer(tanh, mean_squared_error))

# Train:
start = time.time()
net.fit(X_train, y_train, epochs=100, learning_rate=0.1, batch_size=1, shuffle=True)
end = time.time()
print("\nTraining time :", (end - start) * 10 ** 3, "ms")

# Test:
out = net.predict(X_train, to="binary")
print("Result:", out.squeeze())
