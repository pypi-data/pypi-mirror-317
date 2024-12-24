from stensor.nn.module import Module
from stensor.ops import functional as F


class MeanSquaredErrorLoss(Module):
    r"""
    Calculates the mean squared error between the predicted value and the label value.

    For simplicity, let :math:`x` and :math:`y` be 1-dimensional Tensor with length :math:`N`,
    the unreduced loss (i.e. with argument reduction set to 'none') of :math:`x` and :math:`y` is given as:

    .. math::
        \ell(x, y) = L = \{l_1,\dots,l_N\}^\top, \quad \text{with} \quad l_n = (x_n - y_n)^2.

    where :math:`N` is the batch size. If `reduction` is not ``'none'``, then:

    .. math::
        \ell(x, y) =
        \begin{cases}
            \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
            \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}


    """
    def __init__(self):
        super().__init__()

    def forward(self, x, t):
        return F.mean_squared_error(x, t)



class SoftmaxCrossEntropy(Module):
    r"""
    Computes softmax cross entropy between logits and labels.

    Measures the distribution error between the probabilities of the input (computed with softmax function) and the
    labels where the classes are mutually exclusive (only one class is positive) using cross entropy loss.

    Typical input into this function is unnormalized scores denoted as :math:`x` whose shape is :math:`(N, C)` ,
    and the corresponding targets.

    Typically, the input to this function is the fractional value of each category and the corresponding target value,
    and the input format is :math:`(N, C)` .

    For each instance :math:`x_i`, :math:`i` ranges from 0 to N-1, the loss is given as:

    .. math::
        \ell(x_i, c) = - \log\left(\frac{\exp(x_i[c])}{\sum_j \exp(x_i[j])}\right)
        =  -x_i[c] + \log\left(\sum_j \exp(x_i[j])\right)

    where :math:`x_i` is a 1D score Tensor, :math:`c` is the index of 1 in one-hot.

    Args:
        input (Tensor)  Predicted unnormalized logits; see Shape section below for supported shapes.
        target (Tensor)  Ground truth class indices or class probabilities; see Shape section below for supported shapes.
        weight (Tensor, optional)  a manual rescaling weight given to each class. If given, has to be a Tensor of size C
        ignore_index (int, optional)    Specifies a target value that is ignored and does not contribute to the input gradient. 
                                        When size_average is True, the loss is averaged over non-ignored targets. 
                                        Note that ignore_index is only applicable when the target contains class indices. Default: -100
        reduction (str, optional)  Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'. 
                                   'none': no reduction will be applied, 
                                   'mean': the sum of the output will be divided by the number of elements in the output, 
                                   'sum': the output will be summed. 
                                   Note: size_average and reduce are in the process of being deprecated, and in the meantime, 
                                   specifying either of those two args will override reduction. Default: 'mean'

    Note:
        While the labels classes are mutually exclusive, i.e., only one class is positive in the labels, the predicted
        probabilities does not need to be exclusive. It is only required that the predicted probability distribution
        of entry is a valid one.

    """
    def __init__(self, weight=None, ignore_index=-100, reduction='sum'):
        super().__init__()
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, x, t):
        return F.softmax_cross_entropy(x, t, reduction=self.reduction)
