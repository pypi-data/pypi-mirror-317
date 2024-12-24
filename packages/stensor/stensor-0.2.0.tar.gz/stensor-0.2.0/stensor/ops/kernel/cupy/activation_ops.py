import cupy as cp

from stensor import Config
from .cupy_kernel import CupyKernel
from ._impl import softmax, logsumexp


class Sigmoid(CupyKernel):
    def forward(self, x):
        # y = 1 / (1 + cp.exp(-x))
        y = cp.tanh(x * 0.5) * 0.5 + 0.5  # Better implementation
        return y

    def backward(self, gy):
        y = self.outputs[0]().data
        gx = gy * y * (1 - y)
        return gx


class ReLU(CupyKernel):
    def forward(self, x):
        y = cp.maximum(x, 0.0)
        return y

    def backward(self, gy):
        mask = self.inputs[0]().data > 0
        gx = gy * mask
        return gx


class LeakyReLU(CupyKernel):
    def __init__(self, slope):
        self.slope = slope

    def forward(self, x):
        y = x.copy()
        y[x <= 0] *= self.slope
        return y

    def backward(self, gy):
        mask = (self.inputs[0]().data > 0).astype(gy.dtype)
        mask[mask <= 0] = self.slope
        gx = gy * mask
        return gx


class Tanh(CupyKernel):
    def forward(self, x):
        y = cp.tanh(x)
        return y

    def backward(self, gy):
        y = self.outputs[0]().data
        gx = gy * (1 - y * y)
        return gx


class Softmax(CupyKernel):
    def __init__(self, axis=-1):
        self.axis = axis

    def forward(self, x):
        y = softmax(x, self.axis)
        return y

    def backward(self, gy):
        y = self.outputs[0]().data
        gx = y * gy
        sumdx = gx.sum(axis=self.axis, keepdims=True)
        gx -= y * sumdx
        return gx


class LogSoftmax(CupyKernel):
    def __init__(self, axis=1):
        self.axis = axis

    def forward(self, x):
        log_z = logsumexp(x, self.axis)
        y = x - log_z
        return y

    def backward(self, gy):
        y = self.outputs[0]().data
        gx = gy - cp.exp(y) * gy.sum(axis=self.axis, keepdims=True)
        return gx


class SiLU(CupyKernel):
    def forward(self, x):
        # y = 1 / (1 + cp.exp(-x))
        self.sigmoid = cp.tanh(x * 0.5) * 0.5 + 0.5  # Better implementation
        return self.sigmoid * x

    def backward(self, gy):
        if Config.recomputer:
            self.sigmoid = cp.tanh(self.inputs[0]().data * 0.5) * 0.5 + 0.5
        x = self.inputs[0]().data
        return gy * (x * self.sigmoid * (1 - self.sigmoid) + self.sigmoid)


class Swish(CupyKernel):
    def forward(self, x, beta=1.0):
        self.beta_sigmoid = 1 / (1 + cp.exp(-(beta *x)))
        return self.beta_sigmoid * x

    def backward(self, gy):
        x, beta = self.inputs[0]().data, self.inputs[1]().data
        if Config.recomputer:
            self.beta_sigmoid = 1 / (1 + cp.exp(-(beta *x)))
        dx = (x * beta * self.beta_sigmoid * (1 - self.beta_sigmoid) + self.beta_sigmoid)
        dbeta = x * self.beta_sigmoid * (1 - self.beta_sigmoid)
        return gy * dx, gy * dbeta
