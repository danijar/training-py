import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa
import matplotlib.pyplot as plt


def generate_dataset(size=1000):
    dims = 3
    mean = np.zeros(dims)
    cov = [[2, 0, 0], [0, 2, 0], [5, 5, 2]]
    cov = np.array(cov)
    dist = np.random.multivariate_normal(mean, cov, size)
    np.random.shuffle(dist)
    data, target = dist[:, :dims - 1], dist[:, dims - 1]
    return data, target


def visualize(ax, data, target, pred):
    ax.clear()
    x = data[:, 0]
    y = data[:, 1]
    ax.scatter(x, y, target, c='b')
    ax.scatter(x, y, pred, c='r')


class LinearRegression:

    def __init__(self, dims=2):
        self.params = np.random.normal(0, 0.1, dims + 1)
        self.inputs = None

    def predict(self, data):
        bias = np.ones((len(data), 1))
        self.inputs = np.concatenate([bias, data], axis=1)
        pred = np.dot(self.inputs, self.params)
        return pred

    def fit(self, data, target, alpha=1e-5):
        pred = self.predict(data)
        delta_cost = pred - target
        gradient = np.dot(delta_cost[None, :], self.inputs)
        gradient = gradient.sum(axis=0)
        assert gradient.shape == self.params.shape
        self.params -= alpha * gradient
        cost = (pred - target) ** 2 / 2
        cost = cost.sum() / len(cost)
        return cost


if __name__ == '__main__':
    data, target = generate_dataset()
    split = int(0.666 * len(data))
    train_data, test_data = data[:split], data[split:]
    train_target, test_target = target[:split], target[split:]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')
    plt.ion()
    plt.show()

    model = LinearRegression()
    for _ in range(100):
        cost = model.fit(train_data, train_target)
        pred = model.predict(test_data)
        assert pred.shape == test_target.shape
        visualize(ax, test_data, test_target, pred)
        input('Cost {} Press any key'.format(cost))
