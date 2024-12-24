import numpy as np
from stensor.common import Tensor
from stensor.ops.operations.kernel.numpy.numpy_kernel import NumpyKernel
from stensor.ops.operations.kernel.numpy._impl import sum_to


class Reshape(NumpyKernel):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        y = x.reshape(self.shape)
        return y

    def backward(self, gy):
        gx = gy.reshape(self.x_shape)
        return gx


class SumTo(NumpyKernel):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        y = sum_to(x, self.shape)
        return y

    def backward(self, gy):
        gx = np.broadcast_to(gy, self.x_shape)
        return gx


class BroadcastTo(NumpyKernel):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        y = np.broadcast_to(x, self.shape)
        return y

    def backward(self, gy):
        gx = sum_to(gy, self.x_shape)
        return gx


class Transpose(NumpyKernel):
    def __init__(self, dim0, dim1):
        self.dim0 = dim0
        self.dim1 = dim1

    def forward(self, x):
        y = np.swapaxes(x, self.dim0, self.dim1)
        return y

    def backward(self, gy):
        return np.swapaxes(gy, self.dim1, self.dim0)


class GetItem(NumpyKernel):
    def __init__(self, slices):
        if isinstance(slices, Tensor):
            self.slices = slices.data
        else: 
            self.slices = slices

    def forward(self, x):
        y = x[self.slices]
        return y

    def backward(self, gy):
        gx = np.zeros(self.xs[0].shape, dtype=gy.dtype)
        np.add.at(gx, self.slices, gy)
        return gx


def reshape_sum_backward(gy, x_shape, axis, keepdims):
    ndim = len(x_shape)
    tupled_axis = axis
    if axis is None:
        tupled_axis = None
    elif not hasattr(axis, 'len'):
        tupled_axis = (axis,)

    if not (ndim == 0 or tupled_axis is None or keepdims):
        actual_axis = [a if a >= 0 else a + ndim for a in tupled_axis]
        shape = list(gy.shape)
        for a in sorted(actual_axis):
            shape.insert(a, 1)
    else:
        shape = gy.shape

    gy = gy.reshape(shape)
    return gy


class Sum(NumpyKernel):
    def __init__(self, axis, keepdims):
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        self.x_shape = x.shape
        y = x.sum(axis=self.axis, keepdims=self.keepdims)
        return y

    def backward(self, gy):
        gy = reshape_sum_backward(gy, self.x_shape, self.axis,
                                        self.keepdims)
        gx = np.broadcast_to(gy, self.x_shape)
        return gx


def max_backward_shape(x, axis):
    if axis is None:
        axis = range(x.ndim)
    elif isinstance(axis, int):
        if axis < 0:
            axis = x.ndim + axis
        axis = (axis,)
    else:
        axis = axis

    shape = [s if ax not in axis else 1 for ax, s in enumerate(x.shape)]
    return shape


class Max(NumpyKernel):
    def __init__(self, axis=None, keepdims=True):
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        values = np.max(x, axis=self.axis, keepdims=self.keepdims)
        indices = np.argmax(x, axis=self.axis, keepdims=self.keepdims)
        return values, indices

    def backward(self, gvalues, gindices):
        x = self.xs[0]
        y = self.ys[0]

        shape = max_backward_shape(x, self.axis)
        gvalues = np.reshape(gvalues, shape)
        y = np.reshape(y, shape)
        cond = (x == y)
        gvalues = np.broadcast_to(gvalues, cond.shape)
        return gvalues * cond, np.zeros_like(gindices)


class Min(Max):
    def forward(self, x):
        values = np.min(x, axis=self.axis, keepdims=self.keepdims)
        indices = np.argmin(x, axis=self.axis, keepdims=self.keepdims)
        return values, indices


class Clip(NumpyKernel):
    def __init__(self, x_min, x_max):
        self.x_min = x_min
        self.x_max = x_max

    def forward(self, x):
        y = np.clip(x, self.x_min, self.x_max)
        return y

    def backward(self, gy):
        x = self.xs[0]
        mask = (x >= self.x_min) * (x <= self.x_max)
        gx = gy * mask
        return gx


class MaskedFill(NumpyKernel):
    def __init__(self, mask, value):
        self.mask = mask
        self.value = value

    def forward(self, x):
        y = np.where(self.mask.data, self.value, x)
        return y

    def backward(self, gy):
        gx = np.where(self.mask.data, 0, gy.data)
        return gx


class Concat(NumpyKernel):
    def __init__(self, axis):
        self.axis = axis

    def forward(self, *tuple_tensor):
        y = np.concatenate(tuple_tensor, axis=self.axis)
        return y

    def backward(self, gy):
        indices = []
        for i, ele in enumerate(self.xs[:-1]):
            if i==0:
                indices.append(ele.shape[self.axis])
            else:
                indices.append(ele.shape[self.axis] + indices[i-1])

        gx = np.split(gy, indices, axis=self.axis)
        return *gx,
