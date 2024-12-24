import numbers
from typing import Union, Optional, Literal

from stensor.ops.primitive import Primitive
from stensor.common import Tensor
from stensor.common._register_for_tensor import tensor_operator_registry
from stensor.ops._type_check import para_check


@para_check
def add(x0: Union[Tensor, numbers.Number], x1: Union[Tensor, numbers.Number]):
    r"""
    Adds other value to input Tensor.

    .. math::

        out_{i} = input_{i} + other_{i}

    Note:
        - One of the two inputs must be a Tensor.
        - when the two inputs have different shapes, they must be able to broadcast to a same shape.

    """
    if isinstance(x0, numbers.Number) and isinstance(x1, numbers.Number):
        raise ValueError("One of the two inputs must be a Tensor, but got two Number.")
    return Primitive("Add")(x0, x1)


@para_check
def sub(x0: Union[Tensor, numbers.Number], x1: Union[Tensor, numbers.Number]):
    r"""
    Minus other value to input Tensor.

    .. math::

        out_{i} = input_{i} - other_{i}

    Note:
        - One of the two inputs must be a Tensor. 
        - when the two inputs have different shapes, they must be able to broadcast to a same shape.

    """
    if isinstance(x0, numbers.Number) and isinstance(x1, numbers.Number):
        raise ValueError("One of the two inputs must be a Tensor, but got two Number.")
    return Primitive("Sub")(x0, x1)


@para_check
def mul(x0: Union[Tensor, numbers.Number], x1: Union[Tensor, numbers.Number]):
    r"""
    Multiplies two tensors element-wise.

    .. math::

        out_{i} = input_{i} * other_{i}

    Note:
        - One of the two inputs must be a Tensor, when the two inputs have different shapes,
        - they must be able to broadcast to a common shape.

    """
    if isinstance(x0, numbers.Number) and isinstance(x1, numbers.Number):
        raise ValueError("One of the two inputs must be a Tensor, but got two Number.")
    return Primitive("Mul")(x0, x1)


@para_check
def div(x0: Union[Tensor, numbers.Number], x1: Union[Tensor, numbers.Number]):
    r"""
    Divides the first input tensor by the second input tensor in floating-point type element-wise.

    .. math::

        out_{i} = input_{i} / other_{i}
    
    Note:
        - One of the two inputs must be a Tensor, when the two inputs have different shapes,
          they must be able to broadcast to a common shape.
        - The two inputs can not be bool type at the same time,
          [True, Tensor(True, bool\_), Tensor(np.array([True]), bool\_)] are all considered bool type.
        - The two inputs comply with the implicit type conversion rules to make the data types
          consistent.

    """
    if isinstance(x0, numbers.Number) and isinstance(x1, numbers.Number):
        raise ValueError("One of the two inputs must be a Tensor, but got two Number.")
    return Primitive("Div")(x0, x1)


@para_check
def neg(x: Tensor):
    r"""
    Returns a tensor with negative values of the input tensor element-wise.

    .. math::

        out_{i} = - input_{i}

    """
    return Primitive("Neg")(x)


@para_check
def pow(x:Tensor, exponent:Union[Tensor, numbers.Number]):
    r"""
    Calculates the `exponent` power of each element in `input`.

    .. math::

        out_{i} = input_{i} ^{ exponent_{i}}

    .. note::
        - Inputs of `input` and `exponent` comply with the implicit type conversion rules to make the
          data types consistent.
        - The inputs must be two tensors or one tensor and one scalar.
        - When the inputs are two tensors,
          dtypes of them cannot be bool at the same time, and the shapes of them can be broadcast.

    """
    return Primitive("Pow")(x, exponent)


@para_check
def sin(x: Tensor):
    r"""
    Computes sine of the input element-wise.

    .. math::

        out_i = \sin(input_i)

    """
    return Primitive("Sin")(x)


@para_check
def cos(x: Tensor):
    r"""
    Computes cosine of input element-wise.

    .. math::
        out_i = \cos(x_i)

    """
    return Primitive("Cos")(x)


@para_check
def tan(x: Tensor):
    r"""
    Computes tangent of `input` element-wise.

    .. math::

        out_i = \tan(input_i)

    """
    return Primitive("Tan")(x)


@para_check
def exp(x: Tensor):
    r"""
    Returns exponential of a tensor element-wise.

    .. math::

        out_i = e^{x_i}

    """
    return Primitive("Exp")(x)


@para_check
def log(x: Tensor):
    r"""
    Returns the natural logarithm of a tensor element-wise.

    .. math::
        y_i = \log_e(x_i)

    """
    return Primitive("Log")(x)


@para_check
def real(x: Tensor):
    r"""
    """
    return Primitive("Real")(x)


@para_check
def imag(x: Tensor):
    r"""

    """
    return Primitive("Imag")(x)


@para_check
def to_complex(real: Tensor, imag: Tensor):
    r"""

    """
    return Primitive("ToComplex")(real, imag)


@para_check
def to_real(x: Tensor):
    r"""

    """
    return Primitive("ToReal")(x)


@para_check
def eq(x: Tensor, other: Union[Tensor, numbers.Number]):
    r"""
    Computes element-wise equality

    The second argument can be a number or a tensor whose shape is broadcastable with the first argument.

    """
    if isinstance(other, numbers.Number):
        out = (x.data == other)
        return Tensor(out, device=x.device)
    elif isinstance(other, Tensor) and isinstance(other.data, numbers.Number):
        other = Tensor(other.data)

    
    if x.shape == other.shape:
        out = (x.data == other.data)
    else:
        y = broadcast_to(other, x.shape)                                                 
        out = (x.data == y.data)
    return Tensor(out, device=x.device)


@para_check
def gt(x: Tensor, other: Union[Tensor, numbers.Number]):
    r"""
    Computes element-wise equality

    The second argument can be a number or a tensor whose shape is broadcastable with the first argument.

    """

    if isinstance(other, numbers.Number):
        out = (x.data > other)
        return Tensor(out, device=x.device)
    elif isinstance(other, Tensor) and isinstance(other.data, numbers.Number):
        other = Tensor(other.data)

    if x.shape == other.shape:
        out = (x.data > other.data)
    else:
        y = broadcast_to(other, x.shape)                                                 
        out = (x.data > y.data)
    return Tensor(out, device=x.device)


@para_check
def ge(x: Tensor, other: Union[Tensor, numbers.Number]):
    r"""
    Computes element-wise equality

    The second argument can be a number or a tensor whose shape is broadcastable with the first argument.
    
    """
    if isinstance(other, numbers.Number):
        out = (x.data >= other)
        return Tensor(out, device=x.device)
    elif isinstance(other, Tensor) and isinstance(other.data, numbers.Number):
        other = Tensor(other.data)

    
    if x.shape == other.shape:
        out = (x.data >= other.data)
    else:
        y = broadcast_to(other, x.shape)                                                 
        out = (x.data >= y.data)
    return Tensor(out, device=x.device)


@para_check
def lt(x: Tensor, other: Union[Tensor, numbers.Number]):
    r"""
    Computes element-wise equality

    The second argument can be a number or a tensor whose shape is broadcastable with the first argument.

    """
    if isinstance(other, numbers.Number):
        out = (x.data < other)
        return Tensor(out, device=x.device)
    elif isinstance(other, Tensor) and isinstance(other.data, numbers.Number):
        other = Tensor(other.data)

    
    if x.shape == other.shape:
        out = (x.data < other.data)
    else:
        y = broadcast_to(other, x.shape)                                                 
        out = (x.data < y.data)
    return Tensor(out, device=x.device)


@para_check
def le(x: Tensor, other: Union[Tensor, numbers.Number]):
    r"""
    Computes element-wise equality

    The second argument can be a number or a tensor whose shape is broadcastable with the first argument.

    """
    if isinstance(other, numbers.Number):
        out = (x.data <= other)
        return Tensor(out, device=x.device)
    elif isinstance(other, Tensor) and isinstance(other.data, numbers.Number):
        other = Tensor(other.data)

    
    if x.shape == other.shape:
        out = (x.data <= other.data)
    else:
        y = broadcast_to(other, x.shape)                                                 
        out = (x.data <= y.data)
    return Tensor(out, device=x.device)


@para_check
def matmul(x1: Tensor, x2: Tensor):
    r"""
    Only consider Matrix product of two tensors whose dim less than 5 and greater equal than 2. 

    The behavior depends on the dimensionality of the tensors as follows:

    If both arguments are 2-dimensional, the matrix-matrix product is returned.

    If both arguments are more tha 2-dimensional, the matrix-matrix product in last two dimension is returned.

    And the shape of input and other could be broadcast.

    >>> # matrix x matrix
    >>> tensor1 = Tensor(np.rand.randn(3, 4))
    >>> tensor2 = Tensor(np.rand.randn(4, 2))
    >>> stensor.matmul(tensor1, tensor2).shape
    (3, 2)

    >>> # batched matrix x matrix
    >>> tensor1 = Tensor(np.rand.randn(2, 3, 4))
    >>> tensor2 = Tensor(np.rand.randn(4, 2))
    >>> stensor.matmul(tensor1, tensor2).shape
    (2, 3, 3)
    
    >>> # matrix x batched matrix
    >>> tensor2 = Tensor(np.rand.randn(3, 4))
    >>> tensor1 = Tensor(np.rand.randn(2, 4, 2))
    >>> stensor.matmul(tensor1, tensor2).shape
    (2, 3, 3)

    >>> # batched matrix x batched matrix
    >>> tensor1 = Tensor(np.rand.randn(2, 3, 4))
    >>> tensor2 = Tensor(np.rand.randn(2, 4, 5))
    >>> stensor.matmul(tensor1, tensor2).shape
    (2, 3, 5)

    """
    return Primitive("MatMul")(x1, x2)


#TODO: dtype system
def Cast(x: Tensor, other):
    r"""
    Cast the input Tensor to given dtype.

    """
    if x.dtype == other.dtype:
        return x
    return Primitive("Cast", other)(x)


@para_check
def reshape(x: Tensor, shape: tuple[int]):
    r"""
    Rearranges the input Tensor based on the given shape.

    The 'shape' can only have one -1 at most, in which case it's inferred from the remaining dimensions and
    the number of elements in the input.

    """
    if x.shape == shape:
        return x
    return Primitive("Reshape", shape)(x)


@para_check
def expand_dims(x: Tensor, axis: int):
    """
    Adds an additional dimension to `input_x` at the given axis, the dimension
    of `input_x` should be greater than or equal to 1.

    Note:
        If the specified axis is a negative number, the index is counted
        backward from the end and starts at 1.

    """
    shape = list(x.shape)
    shape.insert(axis, 1)
    shape = tuple(shape)
    return Primitive("Reshape", shape)(x)


@para_check
def unsqueeze(x: Tensor, axis: int):
    """
    Adds an additional dimension to `input` at the given dim.

    Note:
        The value of `dim` must be in the range `[-input.ndim-1, input.ndim]`.
        Only constant value is allowed.

    """
    shape = list(x.shape)
    shape.insert(axis, 1)
    shape = tuple(shape)
    return Primitive("Reshape", shape)(x)


@para_check
def squeeze(x: Tensor, dim: Union[int, list[int], tuple[int]]=None):
    """
    Return the Tensor after deleting the dimension of size 1 in the specified `dim`.

    If :math:`dim=None`, it will remove all the dimensions of size 1.
    If `dim` is specified, it will remove the dimensions of size 1 in the given `dim`.
    For example, if the dimension is not specified :math:`dim=None`, input shape is (A, 1, B, C, 1, D),
    then the shape of the output Tensor is (A, B, C, D). If the dimension is specified, the squeeze operation
    is only performed in the specified dimension. If input shape is (A, 1, B), input Tensor will be changed
    to (A, B) when :math:`dim=1`, but when :math:`dim=0` or :math:`dim=2`, an error will occur.

    Note:
        - Squeezing a dimension that is not 1 will raise an error.
        - Please note that in dynamic graph mode, the output Tensor will share data with the input Tensor,
          and there is no Tensor data copy process.
        - The dimension index starts at 0 and must be in the range `[-input.ndim, input.ndim]`.

    """
    if dim is not None:
        shape = [ele for i, ele in enumerate(x.shape) if dim != i or x.shape[i] != 1 ]
        shape = tuple(shape)
        return Primitive("Reshape", shape)(x)
    else:    
        shape = [ele for i, ele in enumerate(x.shape) if ele != 1]
        shape = tuple(shape)
        return Primitive("Reshape", shape)(x)


@para_check
def flatten(x: Tensor, start_dim: int=0, end_dim: int=-1):
    r"""
    Flatten a tensor along dimensions from `start_dim` to `end_dim`.
    """
    shape = list(x.shape)
    if end_dim == -1:
        end_dim = len(x) + 1
    shape[start_dim: end_dim] = (-1,)
    shape = tuple(shape)
    return Primitive("Reshape", shape)(x)


@para_check
def broadcast_to(x: Tensor, shape: tuple[int]):
    r"""
    Broadcasts input tensor to a given shape. The dim of input shape must be smaller
    than or equal to that of target shape. Suppose input shape is :math:`(x_1, x_2, ..., x_m)`,
    target shape is :math:`(*, y_1, y_2, ..., y_m)`, where :math:`*` means any additional dimension.
    The broadcast rules are as follows:

    Compare the value of :math:`x_m` and :math:`y_m`, :math:`x_{m-1}` and :math:`y_{m-1}`, ...,
    :math:`x_1` and :math:`y_1` consecutively and
    decide whether these shapes are broadcastable and what the broadcast result is.

    If the value pairs at a specific dim are equal, then that value goes right into that dim of output shape.
    With an input shape :math:`(2, 3)`, target shape :math:`(2, 3)` , the inferred output shape is :math:`(2, 3)`.

    If the value pairs are unequal, there are three cases:

    Case 1: If the value of the target shape in the dimension is -1, the value of the
    output shape in the dimension is the value of the corresponding input shape in the dimension.
    With an input shape :math:`(3, 3)`, target
    shape :math:`(-1, 3)`, the output shape is :math:`(3, 3)`.

    Case 2: If the value of target shape in the dimension is not -1, but the corresponding
    value in the input shape is 1, then the corresponding value of the output shape
    is that of the target shape. With an input shape :math:`(1, 3)`, target
    shape :math:`(8, 3)`, the output shape is :math:`(8, 3)`.

    Case 3: If the corresponding values of the two shapes do not satisfy the above cases,
    it means that broadcasting from the input shape to the target shape is not supported.

    So far we got the last m dims of the outshape, now focus on the first :math:`*` dims, there are
    two cases:

    If the first :math:`*` dims of output shape does not have -1 in it, then fill the input
    shape with ones until their length are the same, and then refer to
    Case 2 mentioned above to calculate the output shape. With target shape :math:`(3, 1, 4, 1, 5, 9)`,
    input shape :math:`(1, 5, 9)`, the filled input shape will be :math:`(1, 1, 1, 1, 5, 9)` and thus the
    output shape is :math:`(3, 1, 4, 1, 5, 9)`.

    If the first :math:`*` dims of output shape have -1 in it, it implies this -1 is corresponding to
    a non-existing dim so they're not broadcastable. With target shape :math:`(3, -1, 4, 1, 5, 9)`,
    input shape :math:`(1, 5, 9)`, instead of operating the dim-filling process first, it raises errors directly.

    """
    if x.shape == shape:
        return x
    return Primitive("BroadcastTo", shape)(x)


@para_check
def sum_to(x: Tensor, shape: tuple[int]):
    r"""
    The inverse operation of BroadcastTo.

    """
    if x.shape == shape:
        return x
    return Primitive("SumTo", shape)(x)


@para_check
def repeat(x: Tensor, repeat_times: tuple[int]):
    r"""
    Repeats tensor along the specified dimensions.
    new shape : (x.shape[i] * repeat_times[i])
    """
    if all(item==1 for item in repeat_times):
        return x
    res = x
    for i, item in enumerate(repeat_times):
        assert item >= 1
        if item > 1:
            res = Primitive("Concat", i)(*[res for j in range(item)])
        
    return res


@para_check
def repeat_interleave(x: Tensor, repeats: int, dim: int):
    r"""
    Repeats tensor along the specified dimensions.
    Args:
    input (Tensor): the input tensor.
    repeats (int):  The number of repetitions for each element. repeats is broadcasted to fit the shape of the given axis.
    dim (int):  The dimension along which to repeat values. By default, 
                use the flattened input array, and return a flat output array.
    """
    assert repeats > 0
    if repeats == 1:
        return x   
    return Primitive("RepeatInterleave", repeats, dim)(x)


@para_check
def transpose(x: Tensor, dim0: int, dim1: int):
    r"""
    Permutes the dimensions of the input tensor according to input permutation.

    Returns a tensor that is a transposed version of input. The given dimensions dim0 and dim1 are swapped.

    If input is a strided tensor then the resulting out tensor shares its underlying storage with the input tensor, 
    so changing the content of one would change the content of the other.
    """
    return Primitive("Transpose",dim0, dim1)(x)


#@para_check
def get_item(x: Tensor, slices:Union[int, slice, tuple[slice], Tensor]):
    return Primitive("GetItem", slices)(x)


@para_check
def sum(x: Tensor, axis: Union[list, tuple, numbers.Number]=None, keepdims: Union[bool]=False):
    r"""
    Return sum of array elements over a given axis.
    """
    return Primitive("Sum", axis, keepdims)(x)


@para_check
def mean(x: Tensor, axis: Union[list, tuple, numbers.Number]=None, keepdims: Union[bool]=False):
    r"""
    Return mean of array elements over a given axis.
    """
    return Primitive("Mean", axis, keepdims)(x)


@para_check
def max(x: Tensor, axis: Union[list, tuple, numbers.Number]=None, keepdims: Union[bool]=False):
    r"""
    Calculates the maximum value along with the given axis for the input tensor. It returns the maximum values and
    indices.

    .. warning::
        - If there are multiple maximum values, the index of the first maximum value is used.
        - The value range of "axis" is [-dims, dims - 1]. "dims" is the dimension length of "input".

    """
    return Primitive("Max", axis, keepdims)(x)


@para_check
def min(x: Tensor, axis: Union[list, tuple, numbers.Number]=None, keepdims: Union[bool]=False):
    r"""
    Calculates the minimum value along with the given axis for the input tensor. It returns the minimum values and
    indices.

    .. warning::
        - If there are multiple minimum values, the index of the first minimum value is used.
        - The value range of "axis" is [-dims, dims - 1]. "dims" is the dimension length of "x".
    """
    return Primitive("Min", axis, keepdims)(x)


@para_check
def norm(x: Tensor, ord: Union[int, str, None]=None, 
        axis: Union[list, tuple, numbers.Number, None]=None, keepdims: Union[bool]=False):
    r"""
    Calculates the norm value along with the given axis for the input tensor. It returns the norm values.
    
    Args:
    x: input array.
    ord: Specifies the order of the norm, which can be a positive integer, infinity (np.inf),'fro' (Frobenius norm), 
         or None (default'euclidean' or 2).
    axis: Specifies the axis along which the norm is calculated, which can be an integer, tuple, or None.
    keepdims: Boolean value. If true, the axis of the calculated norm is retained in the result array.
    """
    return Primitive("Norm", ord, axis, keepdims)(x)


@para_check
def clip(x:Tensor, x_min:Union[int, float], x_max:Union[int, float]):
    r"""
    Clamps all elements in `x` into the range `[min, max]`.
    """
    return Primitive("Clip", x_min, x_max)(x)

@para_check
def ones_like(x:Tensor):
    r"""

    """
    return Primitive("OnesLike")(x)

@para_check
def zeros_like(x:Tensor):
    r"""

    """
    return Primitive("ZerosLike")(x)

@para_check
def masked_fill(x: Tensor, mask: Tensor, value: numbers.Number):
    r"""
    Fills elements of Tensor with value where mask is True.

    The shapes of `input_x` and `mask` need to be the same or broadcastable.

    """
    return Primitive("MaskedFill", mask, value)(x)


#@para_check
def concat(sequence_of_Tensors:tuple[Tensor], axis:int=-1):
    r"""
    Connect input tensors along with the given axis.

    The input data is a tuple or a list of tensors. These tensors have the same rank :math:`R`.
    Set the given axis as :math:`m`, and :math:`0 \le m < R`. Set the number of input tensors as :math:`N`.
    For the :math:`i`-th tensor :math:`t_i`, it has the shape of :math:`(x_1, x_2, ..., x_{mi}, ..., x_R)`.
    :math:`x_{mi}` is the :math:`m`-th dimension of the :math:`t_i`. Then, the shape of the output tensor is

    .. math::

        (x_1, x_2, ..., \sum_{i=1}^Nx_{mi}, ..., x_R)

    """
    return Primitive("Concat", axis)(*sequence_of_Tensors)


@para_check
def sigmoid(x: Tensor):
    r"""
    Computes Sigmoid of input element-wise. The Sigmoid function is defined as:

    .. math::

        \text{sigmoid}(input_i) = \frac{1}{1 + \exp(-input_i)}

    where :math:`input_i` is an element of the input.

    """
    return Primitive("Sigmoid")(x)


@para_check
def relu(x: Tensor):
    r"""
    Computes ReLU (Rectified Linear Unit activation function) of input tensors element-wise.

    It returns :math:`\max(input,\  0)` element-wise. Specially, the neurons with the negative output
    will be suppressed and the active neurons will stay the same.

    .. math::

        ReLU(input) = (input)^+ = \max(0, input)


    """
    return Primitive("ReLU")(x)


@para_check
def leaky_relu(x: Tensor, slope: float=0.2):
    r"""
    leaky_relu activation function. The element of `input` less than 0 times `alpha` .

    The activation function is defined as:

    .. math::
        \text{leaky_relu}(input) = \begin{cases}input, &\text{if } input \geq 0; \cr
        {\alpha} * input, &\text{otherwise.}\end{cases}

    where :math:`\alpha` represents the `alpha` parameter.


    """
    return Primitive("LeakyReLU", slope)(x)


@para_check
def tanh(x: Tensor):
    r"""
    Computes hyperbolic tangent of input element-wise. The Tanh function is defined as:

    .. math::

        tanh(x_i) = \frac{\exp(x_i) - \exp(-x_i)}{\exp(x_i) + \exp(-x_i)} = \frac{\exp(2x_i) - 1}{\exp(2x_i) + 1},

    where :math:`x_i` is an element of the input Tensor.

    """
    return Primitive("Tanh")(x)


@para_check
def softmax(x: Tensor, axis: int=-1):
    r"""
    Applies the Softmax operation to the input tensor on the specified axis.
    Suppose a slice in the given axis :math:`x`, then for each element :math:`x_i`,
    the Softmax function is shown as follows:

    .. math::
        \text{output}(x_i) = \frac{\exp(x_i)}{\sum_{j = 0}^{N-1}\exp(x_j)},

    where :math:`N` is the length of the tensor.

    Note:
        - All elements will subtract the maximum value on each axis to avoid data overflows. 

    """
    return Primitive("Softmax", axis)(x)


@para_check
def log_softmax(x: Tensor, axis: int=-1):
    return Primitive("LogSoftmax", axis)(x)


@para_check
def silu(x: Tensor):
    r"""
    Applies the silu linear unit function element-wise.

    .. math::

        \text{silu}(x) = x * \sigma(x),

    where :math:`x_i` is an element of the input, :math:`\sigma(x)` is Sigmoid function.

    .. math::

        \text{sigmoid}(x_i) = \frac{1}{1 + \exp(-x_i)},

    """
    return Primitive("SiLU")(x)


@para_check
def swish(x: Tensor, beta:float=1.0):
    r"""
    Applies the swish linear unit function element-wise.

    .. math::

        \text{swish}(x) = x * \sigma(\beta * x),

    where :math:`x_i` is an element of the input, :math:`\sigma(x)` is Sigmoid function.

    .. math::

        \text{sigmoid}(x_i) = \frac{1}{1 + \exp(-x_i)},

    """
    return Primitive("Swish")(x, beta)


@para_check
def dropout(x: Tensor, p: float=0.5):
    r"""
    During training, randomly zeroes some of the elements of the input tensor
    with probability `p` from a Bernoulli distribution. It plays the role of reducing neuron correlation and
    avoid overfitting. And the return will be multiplied by :math:`\frac{1}{1-p}` during training.
    During the reasoning, this operation returns the same Tensor as the `x`.

    """
    return Primitive("Dropout", p)(x)


#@para_check
def linear(x: Tensor, W: Tensor, b: Tensor=None):
    r"""
    Applies a linear transformation to the incoming data: y = x * W^T + b.
    
    """

    #W = W.T
    return Primitive("Linear")(x, W, b)


def batch_norm(x, gamma, beta, mean, var, decay=0.9, eps=2e-5):
    return Primitive("BatchNorm", mean, var, decay, eps)(x, gamma, beta)


def layer_norm(x, gamma, beta, eps=2e-5):
    return Primitive("LayerNorm", eps)(x, gamma, beta)


def rms_norm(x, gamma, eps=2e-5):
    return Primitive("RMSNorm", eps)(x, gamma)


def conv2d(x, W, b=None, stride=1, pad=0):
    return Primitive("Conv2d", stride, pad)(x, W, b)


def deconv2d(x, W, b=None, stride=1, pad=0, outsize=None):
    return Primitive("Deconv2d", stride, pad, outsize)(x, W, b)


def pooling(x, kernel_size, stride=1, pad=0):
    return Primitive("Pooling", kernel_size, stride, pad)(x)


def average_pooling(x, kernel_size, stride=1, pad=0):
    return Primitive("AveragePooling", kernel_size, stride, pad)(x)


def im2col(x, kernel_size, stride=1, pad=0, to_matrix=True):
    """Extract patches from an image based on the filter.

    Args:
        x (`dezero.Variable` or `ndarray`): Input variable of shape
            `(N, C, H, W)`
        kernel_size (int or (int, int)): Size of kernel.
        stride (int or (int, int)): Stride of kernel.
        pad (int or (int, int)): Spatial padding width for input arrays.
        to_matrix (bool): If True the `col` will be reshaped to 2d array whose
            shape is `(N*OH*OW, C*KH*KW)`

    Returns:
        `dezero.Variable`: Output variable. If the `to_matrix` is False, the
            output shape is `(N, C, KH, KW, OH, OW)`, otherwise
            `(N*OH*OW, C*KH*KW)`.

    Notation:
    - `N` is the batch size.
    - `C` is the number of the input channels.
    - `H` and `W` are the height and width of the input image, respectively.
    - `KH` and `KW` are the height and width of the filters, respectively.
    - `SH` and `SW` are the strides of the filter.
    - `PH` and `PW` are the spatial padding sizes.
    - `OH` and `OW` are the the height and width of the output, respectively.
    """
    return Primitive("Im2col", kernel_size, stride, pad, to_matrix)(x)


def col2im(x, input_shape, kernel_size, stride=1, pad=0, to_matrix=True):
    return Primitive("Col2im", input_shape, kernel_size, stride, pad, to_matrix)(x)


def mean_squared_error(x0, x1):
    return Primitive("MeanSquaredError")(x0, x1)


#@para_check
def softmax_cross_entropy(x: Tensor, t: Tensor, reduction: Literal['mean', 'sum', 'none']='mean'):
    return Primitive("SoftmaxCrossEntropy", reduction)(x, t)


@para_check
def full(shape: Union[tuple, list], value:numbers.Number):
    return Primitive("Full", shape, value)()


@para_check
def triu(x: Tensor, diagonal:int = 1):
    return Primitive("Triu", diagonal)(x)


@para_check
def type_as(x0: Tensor, x1: Tensor):
    if x0.dtype == x1.dtype:
        return x0
    else:
        x0.data = x0.data.astype(x1.dtype)
        return x0
        #return Primitive("TypeAs")(x0, x1)


#@para_check
def cast(x0: Tensor, x1):
    if x0.dtype == x1:
        return x0
    else:
        x0.data = x0.data.astype(x1)
        return x0
        #return Primitive("TypeAs")(x0, x1)


@para_check
def topk(x:Tensor, k: int):
    return Primitive("TopK")(x, k)


@para_check
def multinomial(input_probs:Tensor, num_samples: int):
    return Primitive("Multinomial")(input_probs, num_samples)


# Register for Tensor
# math_ops
tensor_operator_registry.register('__add__', add) # Another implement: setattr(tensor_operator_registry, '__add__', add)
tensor_operator_registry.register('__radd__', add)
tensor_operator_registry.register('__sub__', sub)
tensor_operator_registry.register('__rsub__', sub)
tensor_operator_registry.register('__mul__', mul)
tensor_operator_registry.register('__rmul__', mul)
tensor_operator_registry.register('__div__', div)
tensor_operator_registry.register('__rdiv__', div)
tensor_operator_registry.register('__neg__', neg)
tensor_operator_registry.register('__pow__', pow)
tensor_operator_registry.register('__eq__', eq)
tensor_operator_registry.register('__gt__', gt)
tensor_operator_registry.register('__ge__', ge)
tensor_operator_registry.register('__lt__', lt)
tensor_operator_registry.register('__le__', le)
tensor_operator_registry.register('sin', sin)
tensor_operator_registry.register('cos', cos)
tensor_operator_registry.register('tan', tan)
tensor_operator_registry.register('exp', exp)
tensor_operator_registry.register('log', log)
tensor_operator_registry.register('matmul', matmul)

# common_ops
tensor_operator_registry.register('__getitem__', get_item)
tensor_operator_registry.register('broadcast_to', broadcast_to)
tensor_operator_registry.register('sum_to', sum_to)
tensor_operator_registry.register('reshape', reshape)
tensor_operator_registry.register('squeeze', squeeze)
tensor_operator_registry.register('unsqueeze', unsqueeze)
tensor_operator_registry.register('flatten', flatten)
tensor_operator_registry.register('repeat', repeat)
tensor_operator_registry.register('transpose', transpose)
tensor_operator_registry.register('expand_dims', expand_dims)
tensor_operator_registry.register('sum', sum)
tensor_operator_registry.register('mean', mean)
tensor_operator_registry.register('max', max)
tensor_operator_registry.register('min', min)
tensor_operator_registry.register('norm', norm)
tensor_operator_registry.register('clip', clip)
tensor_operator_registry.register('ones_like', ones_like)
tensor_operator_registry.register('zeros_like', zeros_like)
tensor_operator_registry.register('masked_fill', masked_fill)
tensor_operator_registry.register('concat', concat)
tensor_operator_registry.register('type_as', type_as)
tensor_operator_registry.register('cast', cast)

# activation_ops
tensor_operator_registry.register('sigmoid', sigmoid)
tensor_operator_registry.register('relu', relu)
tensor_operator_registry.register('leaky_relu', leaky_relu)
tensor_operator_registry.register('tanh', tanh)
tensor_operator_registry.register('softmax', softmax)
tensor_operator_registry.register('log_softmax', log_softmax)

