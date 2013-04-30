import numpy as np
from copy import deepcopy
from pybrain.optimization import CMAES

try:
    from pracweb.registry import classifier, corrector
except ImportError:
    # Dummies
    classifier = lambda x: lambda y: y
    corrector = classifier


def nclass_to_nbinary(y):
    dim = len(set(y))
    flags = np.zeros((y.size, dim))
    for i, c in enumerate(y):
        flags[i, c] = 1
    return dim, flags


@corrector("monotone_linear")
class MonotoneLinear(object):
    def __init__(self, x_learn, y_learn, n_classes=0):
        _, y = nclass_to_nbinary(y_learn)
        x = np.swapaxes(x_learn, 1, 2)
        w = np.random.randn(np.shape(x)[2])
        print "x size", x.shape
        print "y size", y.shape

        func = lambda w: np.sum((np.dot(x, w) - y) ** 2) \
                + 10000 * np.sum(np.float32(w < 0)) \
                + np.sum(w ** 2)

        self.weights = np.random.randn(np.shape(x)[2])
        print "weights size", self.weights.shape
        optimizer = CMAES(func, self.weights)
        optimizer.minimize = True
        self.weights = optimizer.learn()[0]

    def __call__(self, x_val):
        print "x size", x_val.shape
        print "weights size", self.weights.shape

        return np.dot(np.swapaxes(x_val, 1, 2), self.weights)

if __name__ == '__main__':
    x_learn = np.round(np.random.random([3,5,4]) * 5)
    y_learn = np.round(np.random.random([3,4]) * 5)
    x_test = np.round(np.random.random([3,5,4]) * 5)

    c = MonotoneLinear(x_learn, y_learn)
    print c.weights
    print c(x_test)