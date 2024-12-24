from __future__ import absolute_import

from stensor.config import Config

try:
    import cupy as cp
    Config.gpu_enable = True
    Config.device = "gpu"
except ImportError:
    Config.gpu_enable = False
    
try:
    import torch_npu
    Config.npu_enable = True
    Config.device = "npu"
except ImportError:
    Config.npu_enable = False


from stensor.config import *
from stensor.common import *
from stensor.dataset import *
from stensor.model import *
from stensor.nn import *
from stensor.ops import *
from stensor import config, common, dataset, model, nn, ops

__all__ = []
__all__.extend(config.__all__)
__all__.extend(common.__all__)
__all__.extend(dataset.__all__)
__all__.extend(model.__all__)
__all__.extend(nn.__all__)
__all__.extend(ops.__all__)
