import numpy as np
from stensor.ops.operations.kernel.numpy.numpy_kernel import NumpyKernel
from stensor.ops.operations.kernel.numpy._impl import softmax, logsumexp


class Sigmoid(NumpyKernel):
    def forward(self, x):
        # y = 1 / (1 + np.exp(-x))
        y = np.tanh(x * 0.5) * 0.5 + 0.5  # Better implementation
        return y

    def backward(self, gy):
        y = self.ys[0]
        gx = gy * y * (1 - y)
        return gx


class ReLU(NumpyKernel):
    def forward(self, x):
        y = np.maximum(x.data, 0.0)
        return y

    def backward(self, gy):
        mask = self.xs[0] > 0
        gx = gy * mask
        return gx


class LeakyReLU(NumpyKernel):
    def __init__(self, slope):
        self.slope = slope

    def forward(self, x):
        y = x.copy()
        y[x <= 0] *= self.slope
        return y

    def backward(self, gy):
        mask = (self.xs[0] > 0).astype(gy.dtype)
        mask[mask <= 0] = self.slope
        gx = gy * mask
        return gx


class Tanh(NumpyKernel):
    def forward(self, x):
        y = np.tanh(x)
        return y

    def backward(self, gy):
        y = self.ys[0]
        gx = gy * (1 - y * y)
        return gx


class Softmax(NumpyKernel):
    def __init__(self, axis=-1):
        self.axis = axis

    def forward(self, x):
        y = softmax(x, self.axis)
        return y

    def backward(self, gy):
        y = self.ys[0]
        gx = y * gy
        sumdx = gx.sum(axis=self.axis, keepdims=True)
        gx -= y * sumdx
        return gx


class LogSoftmax(NumpyKernel):
    def __init__(self, axis=1):
        self.axis = axis

    def forward(self, x):
        log_z = logsumexp(x, self.axis)
        y = x - log_z
        return y

    def backward(self, gy):
        y = self.outputs[0]
        gx = gy - np.exp(y.data) * gy.sum(axis=self.axis, keepdims=True)
        return gx


class SiLU(NumpyKernel):
    def forward(self, x):
        # y = 1 / (1 + np.exp(-x))
        self.sigmoid = np.tanh(x * 0.5) * 0.5 + 0.5  # Better implementation
        return self.sigmoid * x

    def backward(self, gy):
        x = self.xs[0]
        return gy * (x * self.sigmoid * (1 - self.sigmoid) + self.sigmoid)


class Swish(NumpyKernel):
    def forward(self, x, beta=1.0):
        self.beta_sigmoid = 1 / (1 + np.exp(-(beta *x)))
        # self.sigmoid = np.tanh(x * 0.5) * 0.5 + 0.5  # Better implementation
        return self.beta_sigmoid * x

    def backward(self, gy):
        x, beta = self.xs
        dx = (x * beta * self.beta_sigmoid * (1 - self.beta_sigmoid) + self.beta_sigmoid)
        dbeta = x * self.beta_sigmoid * (1 - self.beta_sigmoid)
        return gy * dx, gy * dbeta
