import numpy as np
try:
    import cupy as cp
except ImportError:
    pass
from stensor import Config, Tensor
from stensor.ops import functional as F

device = "cpu"
if Config.gpu_enable:
    xp = cp
    device = "gpu"
else:
    xp = np
    device = "cpu"
   
import numpy as np

def precompute_pos_cis(dim: int, seq_len: int, theta: float = 10000.0):
    # 计算词向量元素两两分组之后，每组元素对应的旋转角度 theta_i
    freqs = 1.0 / (theta ** (xp.arange(0, dim, 2)[:(dim // 2)].astype(xp.float32) / dim))
    # 生成 token 序列索引 t = [0, 1,..., seq_len-1]
    t = xp.arange(seq_len, dtype=xp.float32)
    # freqs.shape = [seq_len, dim // 2]
    freqs = xp.outer(t, freqs)  # 计算 m * theta
    
    # 计算复数的旋转矩阵
    freqs_cis = xp.exp(1j * freqs)  # exp(i * freqs) 等价于 cos(freqs) + i*sin(freqs)
    return Tensor(freqs_cis, requires_grad=False)


def apply_rotary_emb(xq, xk, pos_cis):
    r"""
    Rotary Position Embedding (RoPE) <https://arxiv.org/pdf/2104.09864v5>
    The core idea of RoPE is to multiply the position code and the word vector by using the rotation matrix, 
    so that the word vector not only contains semantic information of the word, 
    but also incorporates the position information. RoPE has the following advantages:

    1) Relative position awareness: RoPE can naturally capture the relative positional relationship between words.
    2) No additional computation is required: the combination of positional coding and word vectors is computationally efficient.
    3) Adaptation to sequences of different lengths: RoPE can flexibly process input sequences of different lengths.
    
    """
    origin_type = xq.dtype
    def unite_shape(pos_cis, x):
        ndim = len(x.shape)
        assert 0 <= 1 < ndim
        assert pos_cis.shape == (x.shape[1], x.shape[-1])
        shape = [d if i == 1 or i == ndim - 1 else 1 for i, d in enumerate(x.shape)]
        return pos_cis.reshape(shape)

    def to_complex(x):
        real_part = x[..., 0]  # 取最后一个维度的第一个部分，实部
        imag_part = x[..., 1]  # 取最后一个维度的第二个部分，虚部
        complex_x = F.to_complex(real_part, imag_part)
        return complex_x

    # xq.shape: [batch_size, seq_len, dim]
    # xq_.shape: [batch_size, seq_len, dim // 2, 2]
    xq_ = to_complex(xq.view(*xq.shape[:-1], -1, 2))
    xk_ =  to_complex(xk.view(*xk.shape[:-1], -1, 2))

    # (seq_len, d_q//2) -> (1, seq_len, 1, d_q//2)
    pos_cis = unite_shape(pos_cis, xq_)
    xq_out = F.to_real(xq_ * pos_cis).reshape(xq.shape)
    xk_out = F.to_real(xk_ * pos_cis).reshape(xk.shape)
    return xq_out.cast(origin_type), xk_out.cast(origin_type)
