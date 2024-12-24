import numbers
import numpy as np

from .numpy_kernel import NumpyKernel
from ._impl import sum_to


def binary_elementwise_outputs(x0, x1, gx0, gx1):
    """
    if input is isintance of numbers (integers, floats, bool, etc.) in binary four fundamental operations, 
    its gradient is unuseful.
    """
    if isinstance(x0, numbers.Number):
        x0 = np.array(x0)
    if isinstance(x1, numbers.Number):
        x1 = np.array(x1)
    x0_shape, x1_shape = x0.shape, x1.shape
    if x0_shape != x1_shape:
        gx0 = sum_to(gx0, x0_shape)
        gx1 = sum_to(gx1, x1_shape)
    return gx0, gx1


class Add(NumpyKernel):
    def forward(self, x0, x1):
        y = x0 + x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        gx0, gx1 = gy, gy
        return binary_elementwise_outputs(x0, x1, gx0, gx1)


class Sub(NumpyKernel):
    def forward(self, x0, x1):
        y = x0 - x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        gx0, gx1 = gy, -gy
        return binary_elementwise_outputs(x0, x1, gx0, gx1)


class Mul(NumpyKernel):
    def forward(self, x0, x1):
        y = x0 * x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        if isinstance(x0, np.ndarray) and isinstance(x1, np.ndarray)  and \
            x0.dtype.kind == 'c' and x1.dtype.kind == 'c' :
            gx0, gx1 = gy * np.conj(x1), gy * np.conj(x0)
        else:
            gx0, gx1 = gy * x1, gy * x0
        return binary_elementwise_outputs(x0, x1, gx0, gx1)

class Div(NumpyKernel):
    def forward(self, x0, x1): 
        y = x0 / x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        gx0 = gy / x1
        gx1 = gy * (-x0 / x1 ** 2)
        return binary_elementwise_outputs(x0, x1, gx0, gx1)


class Neg(NumpyKernel):
    def forward(self, x):
        return -x

    def backward(self, gy):
        return -gy


class Pow(NumpyKernel):
    def forward(self, x, exponent):
        y = x ** exponent
        return y

    def backward(self, gy):
        x, exponent = self.inputs[0]().data, self.inputs[1]().data
        gx = exponent * x ** (exponent - 1) * gy
        return gx


class Sin(NumpyKernel):
    def forward(self, x):
        y = np.sin(x)
        return y

    def backward(self, gy):
        gx = gy * (np.cos(self.inputs[0]().data))
        return gx


class Cos(NumpyKernel):
    def forward(self, x):
        y = np.cos(x)
        return y

    def backward(self, gy):
        gx = gy * (-np.sin(self.inputs[0]().data))
        return gx


class Tan(NumpyKernel):
    def forward(self, x):
        y = np.tan(x)
        return y

    def backward(self, gy):
        gx = gy /(np.cos(self.inputs[0]().data) ** 2)
        return gx


class Exp(NumpyKernel):
    def forward(self, x):
        y = np.exp(x)
        return y

    def backward(self, gy):
        gx = gy * self.outputs[0]().data
        return gx


class Log(NumpyKernel):
    def forward(self, x):
        y = np.log(x)
        return y

    def backward(self, gy):
        gx = gy / self.inputs[0]().data
        return gx


class Real(NumpyKernel):
    def forward(self, x):
        y = np.real(x)
        return y

    def backward(self, gy):
        gx = gy.astype(self.inputs[0]().data.dtype)
        return gx


class Imag(NumpyKernel):
    def forward(self, x):
        y = np.imag(x)
        return y

    def backward(self, gy):
        #gx = gy.astype(self.inputs[0]().data.dtype)
        return np.zeros_like(gy)


class ToComplex(NumpyKernel):
    def forward(self, real, imag):
        y = (real + 1j * imag).astype(np.complex64)
        return y

    def backward(self, gy):
        return np.real(gy).astype(self.inputs[0]().data.dtype), np.imag(gy).astype(self.inputs[0]().data.dtype)


class ToReal(NumpyKernel):
    def forward(self, x):
        if not np.iscomplexobj(x):
            raise ValueError("Input must be a complex numpy array.")
        # 将复数数组的实部和虚部分开
        real = x.real
        imag = x.imag
        # 将实部和虚部堆叠在一起形成新的实数数组
        return np.stack((real, imag), axis=-1)

    def backward(self, gy):
        grad_real_part = gy[..., 0]
        grad_imag_part = gy[..., 1]
        # 将实部和虚部的梯度组合成复数张量上的梯度
        return grad_real_part + 1j * grad_imag_part


class MatMul(NumpyKernel):
    def forward(self, x1, x2):
        y = np.matmul(x1, x2)
        return y

    def backward(self, gy):
        x1, x2 = self.inputs[0]().data, self.inputs[1]().data
        #only consider the dim of x or W less than 5.
        gx1 = np.matmul(gy, np.swapaxes(x2, -1, -2))
        if gx1.shape != x1.shape:
            gx1 = sum_to(gx1, x1.shape)

        gx2 = np.matmul(np.swapaxes(x1, -1, -2), gy)
        if gx2.shape != x2.shape:
            gx2 = sum_to(gx2, x2.shape)

        return gx1, gx2


class Full(NumpyKernel):
    def __init__(self, shape, value):
        self.shape = shape
        self.value = value
        
    def forward(self):
        return np.full(self.shape, self.value)

    def backward(self, gy):
        raise NotImplementedError


class Triu(NumpyKernel):
    def __init__(self, diagonal=1):
        self.diagonal = diagonal
        
    def forward(self, x):
        return np.triu(x, k=self.diagonal)

    def backward(self, gy):
        raise NotImplementedError
