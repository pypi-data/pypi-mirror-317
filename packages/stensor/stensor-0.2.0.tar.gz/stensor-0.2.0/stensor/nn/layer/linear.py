import numpy as np

from stensor.nn.module import Module
from stensor.common import Parameter
from stensor.ops import functional as F


class Linear(Module):
    r"""
    Applies an affine linear transformation to the incoming data: y = x * W^T + b.
    Parameters:
        in_features (int) : size of each input sample
        out_features (int) : size of each output sample
        bias (bool) : If set to False, the layer will not learn an additive bias. Default: True
        dtype : Data type of Parameter. Default: ``np.float32`` .

    """
    def __init__(self, in_size, out_size, bias=True, dtype=np.float32):
        super().__init__()
        self.in_size = in_size
        self.out_size = out_size
        self.dtype = dtype
        self.W = Parameter(np.random.randn(out_size, in_size).astype(self.dtype) * np.sqrt(1 / in_size), name='W')

        if not bias:
            self.b = None
        else:
            self.b = Parameter(np.zeros(out_size, dtype=dtype), name='b')

    def forward(self, x):
        y = F.linear(x, self.W, self.b)
        return y


class Dense(Module):
    r"""
    The dense connected layer.

    Applies dense connected layer for the input. This layer implements the operation as:

    .. math::
        \text{outputs} = \text{activation}(\text{X} * \text{kernel} + \text{bias}),

    where :math:`X` is the input tensors, :math:`\text{activation}` is the activation function passed as the activation
    argument (if passed in), :math:`\text{kernel}` is a weight matrix with the same
    data type as the :math:`X` created by the layer, and :math:`\text{bias}` is a bias vector
    with the same data type as the :math:`X` created by the layer (only if has_bias is True).

    Args:
        in_size (int): The number of channels in the input space.
        out_size (int): The number of channels in the output space.
        weight_init (string) :Initialization method for Parameter, must be 'normal' or 'uniform'.
            Default: 'normal'.
            weight will be initialized using HeUniform.
        bias (bool): Specifies whether the layer uses a bias vector :math:`\text{bias}`. Default: ``True``.
        activation (Union[Module, func, Primitive]): activate function applied to the output of the fully connected
            layer. Default: ``F.relu`` .
        dtype : Data type of Parameter. Default: ``np.float32`` .

    Inputs:
        - **x** (Tensor) - Tensor of shape :math:`(*, in\_channels)`. The `in_size` in `Args` should be equal
          to :math:`in\_channels` in `Inputs`.

    Outputs:
        Tensor of shape :math:`(*, out\_channels)`.

    """
    def __init__(self, in_size, out_size, bias=True, weight_init='normal', activation=F.relu, dtype=np.float32):
        super().__init__()
        self.in_size = in_size
        self.out_size = out_size
        self.dtype = dtype
        if weight_init == 'uniform':
            self.W = Parameter(np.random.uniform(-1.0, 1.0, (self.out_size, self.in_size)).astype(self.dtype)* np.sqrt(1 / self.in_size), name='W')
        elif weight_init == 'normal':
            self.W = Parameter(np.random.normal(0.0, 1.0, (self.out_size, self.in_size)).astype(self.dtype)* np.sqrt(1 / self.in_size), name='W')

        self.activation = activation

        if not bias:
            self.b = None
        else:
            self.b = Parameter(np.zeros(out_size, dtype=dtype), name='b')

    def forward(self, x):
        y = F.linear(x, self.W, self.b)
        return self.activation(y)


class TwoLinearNet(Module):
    def __init__(self, in_size, hidden_size, out_size, activation=F.relu):
        super().__init__()
        self.l1 = Linear(in_size, hidden_size)
        self.l2 = Linear(hidden_size, out_size)
        self.activation = activation
    
    def forward(self, inputs):
        y = self.activation(self.l1(inputs))
        y = self.l2(y)
        return y


# Muti-Layer Perception
class MLP(Module):
    def __init__(self, in_size, hidden_size, fc_output_sizes, activation=F.sigmoid):
        super().__init__()
        self.activation = activation
        self.layers = []
        self.first = Linear(in_size, hidden_size[0])
        self.last = Linear(hidden_size[-1], fc_output_sizes)

        for i in range(len(hidden_size)-1):
            layer = Linear(hidden_size[i], hidden_size[i+1])
            setattr(self, 'l' + str(i), layer)
            self.layers.append(layer)

    def forward(self, x):
        x = self.activation(self.first(x))
        for l in self.layers:
            x = self.activation(l(x))
        return self.last(x)
