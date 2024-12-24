from stensor import Config
from stensor.common import Tensor
import numpy as np
import numbers

try:
    import torch_npu
    import torch
except ImportError:
    pass


class AclopKernel:
    @staticmethod
    def _check_inputs_status(inputs):
        for x in inputs:
            # The input b could be None in F.linear.
            if x is None:
                continue 
            if not isinstance(x, (torch.Tensor, numbers.Number, list, tuple)):
                raise ValueError(f"All inputs should be one of (torch.Tensor, numbers.Number, list, tuple), but got {type(x)}")
            if not isinstance(x, torch.Tensor) and not x.device.type == 'npu':
                raise ValueError(f"All torch.Tensor should be 'npu' device type, but got {x.device.type}")


    @staticmethod
    def _transfer_tensor_args(args):
        new_args = []
        for x in args:
            if isinstance(x, Tensor):
                x = x.data
            print("AclopKernel _transfer_tensorinput: ", x, type(x))
            if isinstance(x, (np.ndarray)):
                x = torch.tensor(x, dtype=torch.float32, requires_grad=False).npu()
            new_args.append(x)
        return new_args
    
    def _check_and_transfer_input_status(self, xs):
        new_xs = []
        for x in xs:
            if isinstance(x, np.ndarray):
                x = torch.tensor(x, dtype=torch.float32, requires_grad=True).npu()
            if isinstance(x, torch.Tensor):
                requires_grad = x.requires_grad or Config.enable_backprop
                x = x.clone().detach().requires_grad_(requires_grad)
            new_xs.append(x)
        return new_xs

    def forward(self, *xs):
        xs = self._check_and_transfer_input_status(xs)
        ys = self.inner_forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)
        self.xs1 = xs
        self.ys1 = ys
        return ys

    def backward(self, *gys):
        if not Config.recomputer:
            ys = self.ys1
            #self.xs = self._check_and_transfer_input_status(self.xs)
        else:
            ys = self.forward(*self.xs)
        for x in self.xs1:
            x.retain_grad()
        for gy, y in zip(gys, ys):
            gy = torch.tensor(gy, dtype=torch.float32).npu()
            y.backward(gy)
        return *[x.grad for x in self.xs1],