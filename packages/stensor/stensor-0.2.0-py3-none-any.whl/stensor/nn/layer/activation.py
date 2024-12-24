from stensor.nn.module import Module
from stensor.ops import functional as F


class Sigmoid(Module):
    r"""
    Applies sigmoid activation function element-wise.

    Sigmoid function is defined as:

    .. math::

        \text{sigmoid}(x_i) = \frac{1}{1 + \exp(-x_i)},

    where :math:`x_i` is the element of `x`.

    Inputs:
        - **input** (Tensor) - `input` is :math:`x` in the preceding formula. Tensor of any dimension,
          the data type is float16, float32, float64, complex64 or complex128.

    Outputs:
        Tensor, with the same type and shape as the `input`.


    """
    def __init__(self):
        super(Sigmoid, self).__init__()
        self.softmax = F.sigmoid

    def forward(self, x):
        return self.softmax(x)


class ReLU(Module):
    r"""
    Rectified Linear Unit activation function for complex-valued input.

    Applies ReLU activation layer for the complex-valued input. This layer applies the element-wise
    :math:`\max(0, x)` for both real and imaginary parts of the input tensor independently:

     .. math::
        \begin{align}
        \text{Re(out)} = (Re(inp))^+ = \max(0, Re(inp))\\
        \text{Im(out)} = (Im(inp))^+ = \max(0, Im(inp)),
        \end{align}

    Inputs:
        - **inp** (Tensor) - The input of ReLU is a Tensor of shape (2, *, ..., *), with float16 or float32 data type,
          or (*, ..., *), with complex64 data type.

    Outputs:
        Tensor, with the same data type and shape as the `inp`.

    """
    def __init__(self):
        super(ReLU, self).__init__()
        self.relu = F.relu

    def forward(self, x):
        return self.relu(x)


class LeakyReLU(Module):
    r"""
    Leaky ReLU activation function.

    The activation function is defined as:

    .. math::
            \text{leaky_relu}(x) = \begin{cases}x, &\text{if } x \geq 0; \cr
            {\alpha} * x, &\text{otherwise.}\end{cases}

    where :math:`\alpha` represents the `alpha` parameter.

    For more details, see `Rectifier Nonlinearities Improve Neural Network Acoustic Models
    <https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf>`_.


    Args:
        alpha (Union[int, float]): Slope of the activation function at x < 0. Default: ``0.2`` .

    Inputs:
        - **x** (Tensor) - The input of LeakyReLU is a Tensor of any dimension.

    Outputs:
        Tensor, has the same type and shape as the `x`.

    """
    def __init__(self, slope):
        super(LeakyReLU, self).__init__()
        self.slope = slope
        self.leaky_relu = F.leaky_relu

    def forward(self, x):
        return self.leaky_relu(x, self.slope)


class SiLU(Module):
    r"""
    Applies the silu linear unit function element-wise.

    .. math::

        \text{SiLU}(x) = x * \sigma(x),

    where :math:`x_i` is an element of the input, :math:`\sigma(x)` is Sigmoid function.

    .. math::

        \text{sigmoid}(x_i) = \frac{1}{1 + \exp(-x_i)},


    Inputs:
        - **input** (Tensor) - `input` is :math:`x` in the preceding formula.
          Input with the data type float16 or float32. Tensor of any dimension.

    Outputs:
        Tensor, with the same type and shape as the `input`.

    """
    def __init__(self):
        super(SiLU, self).__init__()
        self.silu = F.silu

    def forward(self, x):
        return self.silu(x)


class Tanh(Module):
    r"""
    Applies the Tanh function element-wise, returns a new tensor with the hyperbolic tangent of the elements of input,
    The input is a Tensor with any valid shape.

    Tanh function is defined as:

    .. math::
        tanh(x_i) = \frac{\exp(x_i) - \exp(-x_i)}{\exp(x_i) + \exp(-x_i)} = \frac{\exp(2x_i) - 1}{\exp(2x_i) + 1},

    where :math:`x_i` is an element of the input Tensor.

    Inputs:
        - **x** (Tensor) - Tensor of any dimension, input with data type of float16 or float32.

    Outputs:
        Tensor, with the same type and shape as the `x`.

    """
    def __init__(self):
        super(Tanh, self).__init__()
        self.tanh = F.tanh

    def forward(self, x):
        return self.tanh(x)


class Softmax(Module):
    r"""
    Softmax activation function, which is a two-category function :class:`mindspore.nn.Sigmoid` in the promotion of
    multi-classification, the purpose is to show the results of multi-classification in the form of probability.

    Calculate the value of the exponential function for the elements of the input Tensor on the `axis`, and then
    normalized to lie in range [0, 1] and sum up to 1.

    Softmax is defined as:

    .. math::
        \text{softmax}(input_{i}) =  \frac{\exp(input_i)}{\sum_{j=0}^{n-1}\exp(input_j)},

    where :math:`input_{i}` is the :math:`i`-th slice in the given dimension of the input Tensor.

    Args:
        axis (int, optional): The axis to apply Softmax operation, if the dimension of `input` is input.ndim,
            the range of axis is `[-input.ndim, input.ndim)`, -1 means the last dimension. Default: ``-1`` .

    Inputs:
        - **input** (Tensor) - The input of Softmax.

    Outputs:
        Tensor, which has the same type and shape as `input` with values in the range[0, 1].

    """
    def __init__(self, axis=-1):
        super(Softmax, self).__init__()
        self.axis = axis
        self.softmax = F.softmax

    def forward(self, x):
        return self.softmax(x, self.axis)


class LogSoftmax(Module):
    r"""
    Applies the LogSoftmax function to n-dimensional input tensor element-wise.

    The input is transformed by the Softmax function and then by the log function to lie in range[-inf,0).

    Logsoftmax is defined as:

    .. math::

        \text{logsoftmax}(x_i) = \log \left(\frac{\exp(x_i)}{\sum_{j=0}^{n-1} \exp(x_j)}\right)

    Args:
        axis (int): The axis to apply LogSoftmax operation, -1 means the last dimension. Default: ``-1`` .

    Inputs:
        - **x** (Tensor) - The input of LogSoftmax, with float16 or float32 data type.

    Outputs:
        Tensor, which has the same type and shape as `x` with output values in the range[-inf,0).

    """
    def __init__(self, axis=-1):
        super(LogSoftmax, self).__init__()
        self.axis = axis
        self.log_softmax = F.log_softmax

    def forward(self, x):
        return self.log_softmax(x, self.axis)
