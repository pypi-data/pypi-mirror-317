import numpy as np
import numbers
import time

from stensor.config import Config

class NumpyKernel:
    @staticmethod
    def _check_inputs_status(inputs):
        for x in inputs:
            # The input b could be None in F.linear.
            if x is not None and not isinstance(x, (np.ndarray, numbers.Number, list, tuple)):
                raise ValueError(f"All inputs should be one of (np.ndarray, numbers.Number, list, tuple), but got {type(x)}")


    @staticmethod
    def _transfer_tensor_args(args):
        return args


    def __call__(self, *inputs):
        return self.forward(*inputs)


    def forward_outer(self, *inputs):
        if not Config.debug:
            return self.forward(*inputs)
        else:        
            start_time = time.time()
            outputs = self.forward(*inputs)
            end_time = time.time()
            inputs_mem = 0
            for i in inputs:
                if isinstance(i, np.ndarray):
                    inputs_mem += (i.itemsize * i.size)
            outputs_mem = 0
            for i in outputs:
                if isinstance(i, np.ndarray):
                    outputs_mem += (i.itemsize * i.size)
            print(f"for operation: {self.name}, Memory used : {(inputs_mem + outputs_mem)/ (1024 ** 2):.4f} MB, cost tiem : {end_time - start_time}.")
            return outputs

    def backward_outer(self, *inputs):
        return self.backward(*inputs)
