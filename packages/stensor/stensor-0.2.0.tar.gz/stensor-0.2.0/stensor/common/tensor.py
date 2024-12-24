import numpy as np
import numbers

from stensor.config import Config
from stensor.common._register_for_tensor import tensor_operator_registry


array_types = [np.ndarray, np.bool_, np.int_, np.float_, np.complex_]
if Config.gpu_enable:
    import cupy as cp
    array_types.extend((cp.ndarray, cp.bool_, cp.int_, cp.float_,))
    
if Config.npu_enable:
    import torch
    array_types.append(torch.Tensor)


class Tensor:
    """
    Tensor is a data structure that stores an n-dimensional array.
    
    Args:
    input_data (Union[Tensor, Parameter, numbers.Number, tuple, list, numpy.ndarray, cp.ndarray]): The data to be stored. 
    name (str, optional): The name of the tensor. Default: ``None`` .
    requires_grad (bool, optional): Whether the tensor requires gradient computation. Default: ``True`` .
    device(str, optional): the device of the constructed tensor. If None and data is a tensor then the device of data is used. 
                 If None and data is not a tensor then the result tensor is constructed on the current device.

    Outputs:
        Tensor.
    """
    def __init__(self, data, name=None, requires_grad=True, device=None):
        if data is not None:
            if isinstance(data, (Tensor, Parameter)):
                data = data.data
            elif isinstance(data, (list, tuple, numbers.Number)):
                data = data
            elif isinstance(data, tuple(array_types)):
                data = data
            else:
                raise TypeError(f"The input type of 'Tensor' should be one of [Tensor, Parameter, numbers.Number, "\
                                f"tuple, list, numpy.ndarray, cp.ndarray], but got {type(data)}")
        self.data = data
        self.name = name
        self.grad = None
        self.creator = None
        self.generation = 0
        self.requires_grad = requires_grad
        self.device = device

    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    @property
    def size(self):
        return self.data.size

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def item(self):
        return self.data
    
    @property
    def T(self):
        if self.ndim != 2:
            raise ValueError("For operation 'T', the ndim of tensor must be 2, but got {}".format(self.ndim))
        return tensor_operator_registry.get('transpose')(self, 0, 1)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        if self.data is None:
            return 'Tensor(None)'
        info = f"Tensor({self.data}, "
        if hasattr(self.data, "shape") and hasattr(self.data, "dtype"):
            info += f"shape: {self.data.shape}, dtype: {self.data.dtype}, "
        info += f"requires_grad: {self.requires_grad}, device: '{self.device}') "
        return info

    def set_creator(self, func):
        self.creator = func
        self.generation = func.generation + 1

    def cleargrad(self):
        self.grad = None

    def backward(self, *dout, retain_graph=False, retrain_inputs=True):
        if self.creator is None:
            return
        
        if dout != ():
            assert len(dout) == len(self.creator.outputs)
        for i, output in enumerate(self.creator.outputs):
            if dout != ():
                output().grad = dout[i]
            else:
                output().grad = output().ones_like()

        funcs = []
        seen_set = set()
        def add_func(f):
            if f not in seen_set:
                funcs.append(f)
                seen_set.add(f)
                funcs.sort(key=lambda x: x.generation)

        add_func(self.creator)
        while funcs:
            f = funcs.pop()
            # ALl outputs is Tensor.
            gys = [output().grad.data for output in f.outputs]  # output is weakref
            if Config.enable_backprop:
                gxs = f.backward(gys)
                if not isinstance(gxs, tuple):
                    gxs = (gxs,)
                gxs = [Tensor(gx) for gx in gxs]
                for x, gx in zip(f.inputs, gxs):
                    # Only support Tensor gradient.
                    if not x().requires_grad:
                        continue
                    if x().grad is None:
                        x().grad = gx
                    else:
                        x().grad.data = x().grad.data + gx.data

                    if x().creator is not None:
                        add_func(x().creator)
    
            if not retain_graph:
                for y in f.outputs:
                    y().grad = None  # y is weakref

            if not retrain_inputs:
                for f in seen_set:
                    if not retain_graph:
                        for x in f.inputs:
                            if not isinstance(x(), Parameter):
                                x().grad = None
                    f.save_inputs = None

    def __getitem__(self, index):
        out = tensor_operator_registry.get('__getitem__')(self, index)
        return out
    
    def __add__(self, other):
        out = tensor_operator_registry.get('__add__')(self, other)
        return out

    def __radd__(self, other):
        out = tensor_operator_registry.get('__radd__')(other, self)
        return out

    def __sub__(self, other):
        out = tensor_operator_registry.get('__sub__')(self, other)
        return out

    def __rsub__(self, other):
        out = tensor_operator_registry.get('__rsub__')(other, self)
        return out

    def __mul__(self, other):
        out = tensor_operator_registry.get('__mul__')(self, other)
        return out

    def __rmul__(self, other):
        out = tensor_operator_registry.get('__rmul__')(other, self)
        return out

    def __truediv__(self, other):   
        out = tensor_operator_registry.get('__div__')(self, other)
        return out

    def __rtruediv__(self, other):
        out = tensor_operator_registry.get('__rdiv__')(other, self)
        return out

    def __neg__(self):
        out = tensor_operator_registry.get('__neg__')(self)
        return out

    def __pow__(self, other):
        out = tensor_operator_registry.get('__pow__')(self, other)
        return out

    def __rpow__(self, other):
        out = tensor_operator_registry.get('__pow__')(other, self)
        return out

    def __eq__(self, x):
        if x is None:
            return self.data is None
        return tensor_operator_registry.get('__eq__')(self, x)

    def __gt__(self, x):
        return tensor_operator_registry.get('__gt__')(self, x)

    def __ge__(self, x):
        return tensor_operator_registry.get('__ge__')(self, x)
    
    def __lt__(self, x):
        return tensor_operator_registry.get('__gt__')(self, x)

    def __le__(self, x):
        return tensor_operator_registry.get('__ge__')(self, x)

    def sin(self):
        return tensor_operator_registry.get('sin')(self)

    def cos(self):
        return tensor_operator_registry.get('cos')(self)
    
    def tan(self):
        return tensor_operator_registry.get('tan')(self)

    def exp(self):
        return tensor_operator_registry.get('tanh')(self)

    def log(self):
        return tensor_operator_registry.get('log')(self)

    def matmul(self, W):
        return tensor_operator_registry.get('matmul')(self, W)

    def sum_to(self, shape):
        return tensor_operator_registry.get('sum_to')(self, shape)

    def broadcast_to(self, shape):
        return tensor_operator_registry.get('broadcast_to')(self, shape)

    def repeat(self, shape):
        return tensor_operator_registry.get('repeat')(self, shape)

    def reshape(self, shape):
        return tensor_operator_registry.get('reshape')(self, shape)

    def view(self, *shape):
        return tensor_operator_registry.get('reshape')(self, shape)

    def transpose(self, dim0, dim1):
        return tensor_operator_registry.get('transpose')(self, dim0, dim1)

    def expand_dims(self, axis):
        return tensor_operator_registry.get('expand_dims')(self, axis)

    def unsqueeze(self, axis):
        return tensor_operator_registry.get('unsqueeze')(self, axis)

    def squeeze(self, axis):
        return tensor_operator_registry.get('squeeze')(self, axis)

    def flatten(self):
        return tensor_operator_registry.get('flatten')(self)

    def sum(self, axis=None, keepdims=False):
        return tensor_operator_registry.get('sum')(self, axis, keepdims)

    def mean(self, axis=None, keepdims=False):
        return tensor_operator_registry.get('mean')(self, axis, keepdims)

    def max(self, axis=None, keepdims=False):
        return tensor_operator_registry.get('max')(self, axis, keepdims)

    def min(self, axis=None, keepdims=False):
        return tensor_operator_registry.get('min')(self, axis, keepdims)

    def norm(self, ord=None, axis=None, keepdims=False):
        return tensor_operator_registry.get('norm')(self, ord, axis, keepdims)

    def get_item(self, slices):
        return tensor_operator_registry.get('get_item')(self, slices)

    def clip(self, x_min, x_max):
        return tensor_operator_registry.get('clip')(self,  x_min, x_max)

    def ones_like(self):
        return tensor_operator_registry.get('ones_like')(self)

    def zeros_like(self):
        return tensor_operator_registry.get('zeros_like')(self)

    def masked_fill(self, mask, value):
        return tensor_operator_registry.get('masked_fill')(self, mask, value)

    def concat(self, *tuple_tensor, axis=0):
        return tensor_operator_registry.get('concat')(self, tuple_tensor, axis)

    def sigmoid(self):
        return tensor_operator_registry.get('sigmoid')(self)

    def relu(self):
        return tensor_operator_registry.get('relu')(self)

    def leaky_relu(self, slope=0.2):
        return tensor_operator_registry.get('leaky_relu')(self, slope)
    
    def tanh(self):
        return tensor_operator_registry.get('tanh')(self)

    def softmax(self, axis=1):
        return tensor_operator_registry.get('softmax')(self, axis)

    def log_softmax(self, axis=1):
        return tensor_operator_registry.get('log_softmax')(self, axis)

    def type_as(self, other):
        return tensor_operator_registry.get('type_as')(self, other)
    
    def cast(self, dtype):
        return tensor_operator_registry.get('cast')(self, dtype)

    def float(self):
        new_data = Tensor(self.data.copy())
        new_data.data.astype(np.float32)
        return new_data

    def double(self):
        new_data = Tensor(self.data.copy())
        new_data.data.astype(np.float32)
        return new_data
    
    def int(self):
        new_data = Tensor(self.data.copy())
        new_data.data.astype(np.int64)
        return new_data

    def to(self, device):
        if device == "cpu":
            out = self.to_cpu()
        elif device == "gpu":
            out = self.to_gpu()
        elif device.startswith('gpu:'):
            gpu_index = device[4:]
            if not gpu_index.isdigit():
                raise ValueError(f"Invalid gpu index {gpu_index}")
            Config.gpu_index = gpu_index
            out = self.to_gpu()
        elif device == "npu":
            out = self.to_npu()
        else:
            raise ValueError(f"Unsupported device: {device}")
        return out
        
    def to_cpu(self):
        if self.data is None:
            raise ValueError("The data of Tensor is None, so cannot convert to cpu.")
        self.device = "cpu"
        self.data = self.numpy(self.data)
        return self

    def to_gpu(self):
        if self.data is None:
            raise ValueError("The data of Tensor is None, so cannot convert to gpu.")
        self.device = "gpu"
        self.data = self.cupy(self.data)
        return self

    def to_npu(self):
        if self.data is None:
            raise ValueError("The data of Tensor is None, so cannot convert to npu.")
        self.device = "npu"
        self.data = self.npu(self.data)
        return self

    def numpy(self, x):
        if isinstance(x, np.ndarray):
            return x
        elif np.isscalar(x):
            return np.array(x)
        return cp.asnumpy(x)

    def cupy(self, x):
        if not Config.gpu_enable:
            raise Exception('CuPy cannot be loaded. Install CuPy!')
        if isinstance(x, cp.ndarray):
            return x
        return cp.asarray(x)
    
    def npu(self, x):
        if not Config.npu_enable:
            raise Exception('torch_npu cannot be loaded. Install torch_npu!')
        if isinstance(x, torch.Tensor) and x.device.type == 'npu':
            return x
        return torch.from_numpy(x).npu()  


class Parameter(Tensor):
    def __init__(self, data, name=None, requires_grad=True, device=None):
        super().__init__(data, name=None, requires_grad=requires_grad, device=device)


    def __repr__(self):
        if self.data is None:
            return 'Parameter(None)'
        return f"Parameter({self.data}), dtype: {self.data.dtype}, requires_grad: {self.requires_grad}, device: '{self.device}') "


__all__ = ['Tensor', 'Parameter']
