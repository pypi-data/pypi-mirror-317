"""
Numpy operator classes.

A collection of operators to build neural networks or to compute functions.
"""
from __future__ import absolute_import

from .math_ops import (Add, Sub, Mul, Div, Neg, Pow, Sin, Cos, Tan, Exp, Log, Real, Imag, ToComplex, ToReal, MatMul, Full, Triu)
from .common_ops import (BroadcastTo, SumTo, Reshape, Tile, RepeatInterleave, Transpose,
                         GetItem, Sum, Mean, Max, Min, Norm, OnesLike, ZerosLike, Clip, MaskedFill, Concat, Cast)
from .activation_ops import (Sigmoid, ReLU, LeakyReLU, Tanh, Softmax, LogSoftmax, SiLU, Swish)
from .nn_ops import (Linear, BatchNorm, LayerNorm, RMSNorm, Dropout, Conv2d, Deconv2d, Pooling, Pooling2DWithIndexes, \
                     AveragePooling, Im2col, Col2im, MeanSquaredError, SoftmaxCrossEntropy)
from .infer_ops import (TopK, Multinomial)

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
    "Real",
    "Imag",
    "ToComplex",
    "ToReal",
    "MatMul",
    "Full",
    "Triu",

    # common_ops:
    "BroadcastTo",
    "SumTo",
    "Reshape",
    "Tile",
    "RepeatInterleave",
    "Transpose",
    "GetItem",
    "MaskedFill",
    "Sum",
    "Mean",
    "Max",
    "Min",
    "Norm",
    "OnesLike",
    "ZerosLike",
    "Clip",
    "Concat",
    "Cast",

    # activation_ops:
    "Sigmoid",
    "ReLU",
    "Softmax",
    "LogSoftmax",
    "LeakyReLU",
    "Tanh",
    "SiLU",
    "Swish",

    # nn_ops:
    "Linear",
    "BatchNorm",
    "LayerNorm",
    "RMSNorm",
    "Dropout",
    "Conv2d",
    "Deconv2d",
    "Pooling",
    "Pooling2DWithIndexes",
    "AveragePooling",
    "Im2col",
    "Col2im",
    "MeanSquaredError",
    "SoftmaxCrossEntropy",
    
    # infer_ops:
    "TopK",
    "Multinomial",
]

from ..dispatcher import operator_dispatcher
for op in __all__:
    operator_dispatcher.register((op, "cpu"), globals()[op])

print("===load numpy kernel")