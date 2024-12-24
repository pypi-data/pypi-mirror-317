import cupy as cp
import numpy as np
import numbers
import time

from stensor.config import Config
from stensor.common import Tensor


class CupyKernel:
    @staticmethod
    def _check_inputs_status(inputs):
        for x in inputs:
            # The input b could be None in F.linear.
            if x is None:
                continue
            if not isinstance(x, (cp.ndarray, numbers.Number, list, tuple)):
                raise ValueError(f"All inputs should be one of (cp.ndarray, numbers.Number, list, tuple), but got {type(x)}")


    @staticmethod
    def _transfer_tensor_args(args):
        new_args = []
        for x in args:
            if isinstance(x, Tensor):
                x = x.data
            if isinstance(x, (np.ndarray)):
                x = cp.asarray(x)
            new_args.append(x)
        return new_args


    def forward_outer(self, *inputs, **kargs):
        if not Config.debug:
            return self.forward(*inputs, **kargs)
        else:        
            mempool = cp.get_default_memory_pool()
            mempool.free_all_blocks()
            before = mempool.used_bytes()
            start_time = time.time()
            outputs = self.forward(*inputs, **kargs)
            end_time = time.time()
            after = mempool.used_bytes()
            
            array_inputs_info = []
            array_outputs_info = []
            if not isinstance(outputs, tuple):
                ys = (outputs,)
            else:
                ys = outputs
            for i in inputs:
                if isinstance(i, (np.ndarray, cp.ndarray)):
                    array_inputs_info.append((i.shape, i.dtype))
            for j in ys:
                if isinstance(j, (np.ndarray, cp.ndarray)):
                    array_outputs_info.append((j.shape, j.dtype))
            print(f"[forward] for operation: {self.name}, inputs:{array_inputs_info}, outputs:{array_outputs_info}"\
                  f"Memory currentle used: {after/ (1024 ** 2):.4f} MB, Memory increment : {(after - before)/ (1024 ** 2):.4f} MB, "
                  f"cost time : {end_time - start_time:.8f} ")
            return outputs

    def backward_outer(self, *inputs, **kargs):
        if not Config.debug:
            return self.backward(*inputs, **kargs)
        else:        
            mempool = cp.get_default_memory_pool()
            mempool.free_all_blocks()
            before = mempool.used_bytes()
            start_time = time.time()
            outputs = self.backward(*inputs, **kargs)
            end_time = time.time()
            after = mempool.used_bytes()
            
            array_inputs_info = []
            array_outputs_info = []
            if not isinstance(outputs, tuple):
                gxs = (outputs,)
            else:
                gxs = outputs
            for i in inputs:
                if isinstance(i, (np.ndarray, cp.ndarray)):
                    array_inputs_info.append((i.shape, i.dtype))
            for j in gxs:
                if isinstance(j, (np.ndarray, cp.ndarray)):
                    array_outputs_info.append((j.shape, j.dtype))
            print(f"[backward] for operation: {self.name}, inputs:{array_inputs_info}, outputs:{array_outputs_info} "\
                  f"Memory currentle used: {after/ (1024 ** 2):.4f} MB, Memory increment : {(after - before)/ (1024 ** 2):.4f} MB, "
                  f"cost time : {end_time - start_time:.8f} ")
            return outputs