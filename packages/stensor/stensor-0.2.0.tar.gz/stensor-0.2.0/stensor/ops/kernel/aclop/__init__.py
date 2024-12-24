from __future__ import absolute_import

from .math_ops import (Add, Sub, Mul, Div, Neg, Pow, Sin, Cos, Tan, Exp, Log, MatMul,)
# from .common_ops import (BroadcastTo, SumTo, Reshape, Transpose,
#                          GetItem, Sum, Max, Min, Clip, MaskedFill, Concat)
# from .activation_ops import (Sigmoid, ReLU, LeakyReLU, Tanh, Softmax, LogSoftmax, SiLU, Swish)
# from .nn_ops import (Linear, BatchNorm, LayerNorm, RMSNorm, Dropout, Conv2d, Deconv2d, Pooling, Pooling2DWithIndexes, \
#                      AveragePooling, Im2col, Col2im, MeanSquaredError, SoftmaxCrossEntropy)


__all__ = [
    # math_ops:
    "Add",
    "Sub",
    "Mul",
    "Div",
    "Neg",
    "Pow",
    "Sin",
    "Cos",
    "Tan",
    "Exp",
    "Log",
    "MatMul",

    # # common_ops:
    # "BroadcastTo",
    # "SumTo",
    # "Reshape",
    # "Transpose",
    # "GetItem",
    # "MaskedFill",
    # "Sum",
    # "Max",
    # "Min",
    # "Clip",
    # "Concat",

    # # activation_ops:
    # "Sigmoid",
    # "ReLU",
    # "Softmax",
    # "LogSoftmax",
    # "LeakyReLU",
    # "Tanh",
    # "SiLU",
    # "Swish",

    # # nn_ops:
    # "Linear",
    # "BatchNorm",
    # "LayerNorm",
    # "RMSNorm",
    # "Dropout",
    # "Conv2d",
    # "Deconv2d",
    # "Pooling",
    # "Pooling2DWithIndexes",
    # "AveragePooling",
    # "Im2col",
    # "Col2im",
    # "MeanSquaredError",
    # "SoftmaxCrossEntropy",
]
from ..dispatcher import operator_dispatcher
for op in __all__:
    operator_dispatcher.register((op, "npu"), globals()[op])

print("===load aclop kernel")