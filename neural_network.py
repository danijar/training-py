import numpy as np


class Network:

    def __init__(self, num_inputs, num_hidden, num_output,
                 init_weight_scale=0.5):
        self.w1 = np.random.normal(
            0, init_weight_scale, (num_inputs + 1, num_hidden))
        self.w2 = np.random.normal(
            0, init_weight_scale, (num_hidden + 1, num_output))
        self.inputs = None
        self.hidden = None
        self.output = None

    def forward(self, inputs):
        self.inputs = np.insert(inputs, 0, 1)
        self.hidden = self.sigmoid(self.inputs.dot(self.w1))
        self.hidden = np.insert(self.hidden, 0, 1)
        self.output = self.sigmoid(self.hidden.dot(self.w2))
        return self.output

    def backward(self, target):
        # Output layer
        delta_output_out = self.delta_cost(self.output, target)
        delta_output_local = self.delta_sigmoid(self.output)
        self.delta_output = delta_output_out * delta_output_local
        # Hidden layer
        delta_hidden_out = self.delta_output.dot(self.w2.T)[1:]
        delta_hidden_local = self.delta_sigmoid(self.hidden)[1:]
        self.delta_hidden = delta_hidden_local * delta_hidden_out
        # Weights
        self.delta_w2 = np.outer(self.hidden, self.delta_output)
        self.delta_w1 = np.outer(self.inputs, self.delta_hidden)
        assert self.w1.shape == self.delta_w1.shape
        assert self.w2.shape == self.delta_w2.shape

    def gradient_decent(self, learning_rate=0.1):
        self.w1 -= learning_rate * self.delta_w1
        self.w2 -= learning_rate * self.delta_w2

    @staticmethod
    def cost(prediction, target):
        return 0.5 * (prediction - target) ** 2

    @staticmethod
    def delta_cost(prediction, target):
        return prediction - target

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @classmethod
    def delta_sigmoid(cls, x):
        return cls.sigmoid(x) * (1 - cls.sigmoid(x))


if __name__ == '__main__':
    import random

    # XOR dataset
    inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    targets = np.array([[0], [1], [1], [0]])
    dataset = list(zip(inputs, targets))

    network = Network(2, 5, 1, init_weight_scale=1)
    for _ in range(20000):
        cost = 0
        error = 0
        random.shuffle(dataset)
        for input_, target in dataset:
            prediction = network.forward(input_)
            cost += float(network.cost(prediction, 0))
            guess = 0 if prediction[0] < 0.5 else 1
            error += int(guess != target)
            network.backward(target)
            network.gradient_decent(learning_rate=0.1)
        cost /= len(inputs)
        error /= len(inputs)
        print('Cost {:.5f} Error {:.2}'.format(cost, error))
    # Final weights
    print('w1\n', network.w1)
    print('w2\n', network.w2)
