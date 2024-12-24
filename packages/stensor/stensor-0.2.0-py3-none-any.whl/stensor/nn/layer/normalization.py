import numpy as np

from stensor.nn.module import Module
from stensor.common import Parameter
from stensor.ops import functional as F


class Dropout(Module):
    r"""
    Dropout layer for the input.

    Dropout is a means of regularization that reduces overfitting by preventing correlations between neuronal nodes.
    The operator randomly sets some neurons output to 0 according to `p`, which means the probability of discarding
    during training. And the return will be multiplied by :math:`\frac{1}{1-p}` during training.
    During the reasoning, this layer returns the same Tensor as the `x`.

    This technique is proposed in paper `Dropout: A Simple Way to Prevent Neural Networks from Overfitting
    <http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf>`_ and proved to be effective to reduce
    over-fitting and prevents neurons from co-adaptation. See more details in `Improving neural networks by
    preventing co-adaptation of feature detectors
    <https://arxiv.org/pdf/1207.0580.pdf>`_.

    """
    def __init__(self, p):
        super().__init__()
        self.p = p

    def forward(self, x):
        if not self.training or self.p == 0:
            return x

        out = F.dropout(x, p=self.p)
        return out
    

class BatchNorm(Module):
    def __init__(self, decay=0.9, eps=1e-5):
        super().__init__()
        # `.avg_mean` and `.avg_var` are `Parameter` objects, so they will be
        # saved to a file (using `save_weights()`).
        # But they don't need grads, so they're just used as `ndarray`.
        self.avg_mean = Parameter(None, name='avg_mean')
        self.avg_var = Parameter(None, name='avg_var')
        self.gamma = Parameter(None, name='gamma')
        self.beta = Parameter(None, name='beta')
        self.decay = decay
        self.eps = eps

    def _init_params(self, x):
        D = x.shape[1]
        if self.avg_mean.data is None:
            self.avg_mean.data = np.zeros(D, dtype=x.dtype)
        if self.avg_var.data is None:
            self.avg_var.data = np.ones(D, dtype=x.dtype)
        if self.gamma.data is None:
            self.gamma.data = np.ones(D, dtype=x.dtype)
        if self.beta.data is None:
            self.beta.data = np.zeros(D, dtype=x.dtype)

    def forward(self, x):
        if self.avg_mean.data is None:
            self._init_params(x)
        return F.batch_norm(x, self.gamma, self.beta, self.avg_mean.data,
                            self.avg_var.data, self.decay, self.eps)


class LayerNorm(Module):
    r"""
    LayerNorm is mainly used in the NLP domain. It normalizes the feature vector (embedded dimension) of each token.
    """
    def __init__(self, normalized_shape=None, eps=1e-5):
        super().__init__()
        self.eps = eps
        if normalized_shape is None:
            self.gamma = Parameter(None, name='gamma')
            self.beta = Parameter(None, name='beta')
        else:
            self.gamma = Parameter(np.ones(normalized_shape), name='gamma')
            self.beta = Parameter(np.ones(normalized_shape), name='beta')

    def _init_params(self, x):
        D = x.shape[1:]
        if self.gamma.data is None:
            self.gamma.data = np.ones(D, dtype=x.dtype)
        if self.beta.data is None:
            self.beta.data = np.zeros(D, dtype=x.dtype)

    def forward(self, x):
        if self.gamma.data is None:
            self._init_params(x)
        return F.layer_norm(x, self.gamma, self.beta, self.eps)


class RMSNorm(Module):
    r"""
    RMSNorm (Root Mean Square Layer Normalization) <https://openreview.net/pdf?id=SygkZ3MTJE>
    paper assumes that recentralization in LayerNorm is no longer necessary (translation invariance is not important). 
    RMSNorm normalizes the input of each layer of neurons through root mean square (RMS), 
    which makes the model capable of rescaling invariance and implicit learning rate adjustment. 
    
    Compared with LayerNorm, RMSNorm is simpler and can save 7% to 64% of the calculation time.
    """
    def __init__(self, normalized_shape, eps=1e-5, dtype=np.float32):
        super().__init__()
        self.eps = eps
        self.gamma = Parameter(np.ones(normalized_shape, dtype=dtype), name='gamma')

    def forward(self, x):
        return F.rms_norm(x, self.gamma, self.eps)
