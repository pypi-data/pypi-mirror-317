import cupy as cp

from stensor import Config
from stensor.common import Tensor
from .cupy_kernel import CupyKernel
from ._impl import sum_to


class Reshape(CupyKernel):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        y = x.reshape(self.shape)
        return y

    def backward(self, gy):
        if Config.recomputer:
            self.x_shape = self.inputs[0]().data.shape
        gx = gy.reshape(self.x_shape)
        return gx



class Tile(CupyKernel):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        y = cp.tile(x, self.shape)
        return y

    def backward(self, gy):
        x_shape = self.inputs[0]().data.shape
        gx = cp.empty(x_shape, dtype=self.inputs[0]().data.dtype)
        for idx in cp.ndindex(*x_shape):
            gx[idx] = gy[idx]

        times = 1
        for i in self.shape:
            times *= i

        return gx * times


class RepeatInterleave(CupyKernel):
    def __init__(self, repeats, dim):
        self.repeats = repeats
        self.dim = dim

    def forward(self, x):
        y = cp.repeat(x, self.repeats, axis=self.dim)
        return y

    def backward(self, gy):
        x_shape = list(self.inputs[0]().data.shape).copy()
        x_shape.insert(self.dim + 1, self.repeats)
        gx = gy.reshape(x_shape).sum(axis=self.dim + 1)
        return gx


class SumTo(CupyKernel):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        y = sum_to(x, self.shape)
        return y

    def backward(self, gy):
        if Config.recomputer:
            self.x_shape = self.inputs[0]().data.shape
        gx = cp.broadcast_to(gy, self.x_shape)
        return gx


class BroadcastTo(CupyKernel):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        y = cp.broadcast_to(x, self.shape)
        return y

    def backward(self, gy):
        if Config.recomputer:
            self.x_shape = self.inputs[0]().data.shape
        gx = sum_to(gy, self.x_shape)
        return gx


class Transpose(CupyKernel):
    def __init__(self, dim0, dim1):
        self.dim0 = dim0
        self.dim1 = dim1

    def forward(self, x):
        y = cp.swapaxes(x, self.dim0, self.dim1)
        return y

    def backward(self, gy):
        return cp.swapaxes(gy, self.dim1, self.dim0)


class GetItem(CupyKernel):
    def __init__(self, slices):
        if isinstance(slices, Tensor):
            self.slices = slices.data
        else: 
            self.slices = slices    
        
    def forward(self, x):
        y = x[self.slices]
        return y

    def backward(self, gy):
        gx = cp.zeros(self.inputs[0]().data.shape, dtype=gy.dtype)
        # 判断是否需要调整形状
        if gx[self.slices].shape != gy.shape:
            # 使用切片调整 gy 的形状以与 gx[self.slices] 兼容
            gy = gy[tuple(slice(0, s) for s in gx[self.slices].shape)]
        #高效的原地加法：避免额外的内存开销，并确保加法操作不会被重写或冲突。
        cp.add.at(gx, self.slices, gy)
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


class Sum(CupyKernel):
    def __init__(self, axis, keepdims):
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        self.x_shape = x.shape
        y = x.sum(axis=self.axis, keepdims=self.keepdims)
        return y

    def backward(self, gy):
        if Config.recomputer:
            self.x_shape = self.inputs[0]().data.shape
        gy = reshape_sum_backward(gy, self.x_shape, self.axis,
                                        self.keepdims)
        gx = cp.broadcast_to(gy, self.x_shape)
        return gx


class Mean(CupyKernel):
    def __init__(self, axis, keepdims):
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        self.x_shape = x.shape
        y = x.mean(axis=self.axis, keepdims=self.keepdims)
        return y

    def backward(self, gy):
        return NotImplementedError
    

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


class Max(CupyKernel):
    def __init__(self, axis=None, keepdims=True):
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        values = cp.max(x, axis=self.axis, keepdims=self.keepdims)
        indices = x.argmax(axis=self.axis, keepdims=self.keepdims)
        return values, indices

    def backward(self, gvalues, gindices):
        x = self.inputs[0]().data
        y = self.outputs[0]().data

        shape = max_backward_shape(x, self.axis)
        gvalues = cp.reshape(gvalues, shape)
        y = cp.reshape(y, shape)
        cond = (x == y)

        gvalues = cp.broadcast_to(gvalues, cond.shape)
        return gvalues * cond, cp.zeros_like(gindices)


class Min(Max):
    def forward(self, x):
        values = cp.min(x, axis=self.axis, keepdims=self.keepdims)
        indices = cp.argmin(x, axis=self.axis, keepdims=self.keepdims)
        return values, indices


class Norm(CupyKernel):
    def __init__(self, ord=None, axis=None, keepdims=True):
        self.ord = ord
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        y = cp.linalg.norm(x, ord=self.ord, axis=self.axis, keepdims=self.keepdims)
        return y

    def backward(self, gy):
        return NotImplementedError


class OnesLike(NumpyKernel):
    def forward(self, x):
        return cp.ones_like(x)

    def backward(self, gy):
        return gy


class ZerosLike(NumpyKernel):
    def forward(self, x):
        return cp.zeros_like(x)

    def backward(self, gy):
        return cp.zeros_like(gy)


class Clip(CupyKernel):
    def __init__(self, x_min, x_max):
        self.x_min = x_min
        self.x_max = x_max

    def forward(self, x):
        y = cp.clip(x, self.x_min, self.x_max)
        return y

    def backward(self, gy):
        x = self.inputs[0]().data
        mask = (x >= self.x_min) * (x <= self.x_max)
        gx = gy * mask
        return gx


class MaskedFill(CupyKernel):
    def __init__(self, mask, value):
        self.mask = mask
        self.value = value

    def forward(self, x):
        y = cp.where(self.mask, self.value, x)
        return y

    def backward(self, gy):
        gx = cp.where(self.mask, 0, gy)
        return gx


class Concat(CupyKernel):
    def __init__(self, axis):
        self.axis = axis

    def forward(self, *tuple_tensor):
        y = cp.concatenate(tuple_tensor, axis=self.axis)
        return y

    def backward(self, gy):
        indices = []
        for i, ele in enumerate(self.inputs[:-1]):
            if i==0:
                indices.append(ele().shape[self.axis])
            else:
                indices.append(ele().shape[self.axis] + indices[i-1])

        gx = cp.split(gy, indices, axis=self.axis)
        return *gx,


class Cast(CupyKernel):
    def forward(self, x0, x1):
        pass

    def backward(self, gy):
        pass
