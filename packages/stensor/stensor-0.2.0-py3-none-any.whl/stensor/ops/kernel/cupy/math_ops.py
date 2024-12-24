import numbers
import cupy as cp

from .cupy_kernel import CupyKernel
from ._impl import sum_to


def binary_elementwise_outputs(x0, x1, gx0, gx1):
    """
    if input is isintance of numbers (integers, floats, bool, etc.) in binary four fundamental operations, 
    its gradient is None.
    """
    if isinstance(x0, numbers.Number):
        x0 = cp.array(x0)
        return None, gx1
    elif isinstance(x1, numbers.Number):
        x1 = cp.array(x1)
        return gx0, None
    else:
        x0_shape, x1_shape = x0.shape, x1.shape
        if x0_shape != x1_shape:
            gx0 = sum_to(gx0, x0_shape)
            gx1 = sum_to(gx1, x1_shape)
        return gx0, gx1


class Add(CupyKernel):
    def forward(self, x0, x1):
        y = x0 + x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        gx0, gx1 = gy, gy
        return binary_elementwise_outputs(x0, x1, gx0, gx1)


class Sub(CupyKernel):
    def forward(self, x0, x1):
        y = x0 - x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        gx0, gx1 = gy, -gy
        return binary_elementwise_outputs(x0, x1, gx0, gx1)


class Mul(CupyKernel):
    def forward(self, x0, x1):
        y = x0 * x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        if isinstance(x0, cp.ndarray) and isinstance(x1, cp.ndarray)  and \
            x0.dtype.kind == 'c' and x1.dtype.kind == 'c' :
            gx0, gx1 = gy * cp.conj(x1), gy * cp.conj(x0)
        else:
            gx0, gx1 = gy * x1, gy * x0
        return binary_elementwise_outputs(x0, x1, gx0, gx1)


class Div(CupyKernel):
    def forward(self, x0, x1): 
        y = x0 / x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0]().data, self.inputs[1]().data
        gx0 = gy / x1
        gx1 = gy * (-x0 / x1 ** 2)
        return binary_elementwise_outputs(x0, x1, gx0, gx1)


class Neg(CupyKernel):
    def forward(self, x):
        return -x

    def backward(self, gy):
        return -gy


class Pow(CupyKernel):
    def forward(self, x, exponent):
        y = x ** exponent
        return y

    def backward(self, gy):
        x, exponent = self.inputs[0]().data, self.inputs[1]().data
        gx = exponent * x ** (exponent - 1) * gy
        return gx


class Sin(CupyKernel):
    def forward(self, x):
        y = cp.sin(x)
        return y

    def backward(self, gy):
        gx = gy * (cp.cos(self.inputs[0]().data))
        return gx


class Cos(CupyKernel):
    def forward(self, x):
        y = cp.cos(x)
        return y

    def backward(self, gy):
        gx = gy * (-cp.sin(self.inputs[0]().data))
        return gx


class Tan(CupyKernel):
    def forward(self, x):
        y = cp.tan(x)
        return y

    def backward(self, gy):
        gx = gy /(cp.cos(self.inputs[0]().data) ** 2)
        return gx


class Exp(CupyKernel):
    def forward(self, x):
        y = cp.exp(x)
        return y

    def backward(self, gy):
        gx = gy * self.outputs[0]().data
        return gx


class Log(CupyKernel):
    def forward(self, x):
        y = cp.log(x)
        return y

    def backward(self, gy):
        gx = gy / self.inputs[0]().data
        return gx


class Real(CupyKernel):
    def forward(self, x):
        y = cp.real(x)
        return y

    def backward(self, gy):
        gx = gy.astype(self.inputs[0]().data.dtype)
        return gx


class Imag(CupyKernel):
    def forward(self, x):
        y = cp.imag(x)
        return y

    def backward(self, gy):
        return cp.zeros_like(gy)


class ToComplex(CupyKernel):
    def forward(self, real, imag):
        y = (real + 1j * imag).astype(cp.complex64)
        return y

    def backward(self, gy):
        return cp.real(gy).astype(self.inputs[0]().data.dtype), cp.imag(gy).astype(self.inputs[0]().data.dtype)


class ToReal(CupyKernel):
    def forward(self, x):
        if not cp.iscomplexobj(x):
            raise ValueError("Input must be a complex numpy array.")
        # 将复数数组的实部和虚部分开
        real = x.real
        imag = x.imag
        # 将实部和虚部堆叠在一起形成新的实数数组
        return cp.stack((real, imag), axis=-1)

    def backward(self, gy):
        grad_real_part = gy[..., 0]
        grad_imag_part = gy[..., 1]
        # 将实部和虚部的梯度组合成复数张量上的梯度
        return grad_real_part + 1j * grad_imag_part


class MatMul(CupyKernel):
    def forward(self, x1, x2):
        y = cp.matmul(x1, x2)
        return y

    def backward(self, gy):
        x1, x2 = self.inputs[0]().data, self.inputs[1]().data
        #only consider the dim of x or W less than 5.
        gx1 = cp.matmul(gy, cp.swapaxes(x2, -1, -2))
        if gx1.shape != x1.shape:
            gx1 = sum_to(gx1, x1.shape)

        gx2 = cp.matmul(cp.swapaxes(x1, -1, -2), gy)
        if gx2.shape != x2.shape:
            gx2 = sum_to(gx2, x2.shape)

        return gx1, gx2


class Full(CupyKernel):
    def __init__(self, shape, value):
        self.shape = shape
        self.value = value
        
    def forward(self):
        return cp.full(self.shape, self.value)

    def backward(self, gy):
        raise NotImplementedError


class Triu(CupyKernel):
    def __init__(self, diagonal=1):
        self.diagonal = diagonal
        
    def forward(self, x):
        return cp.triu(x, k=self.diagonal)

    def backward(self, gy):
        raise NotImplementedError
