from stensor.config import Config
from .numpy import *

if Config.gpu_enable:
    from .cupy import *
if Config.npu_enable:
    from .aclop import *
