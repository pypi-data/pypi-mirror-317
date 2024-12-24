import pytest
from stensor import Tensor, nn
from stensor.config import Config
from stensor.ops import functional as F
import torch
import numpy as np
import functools
np.random.seed(0)

def check_result(stensor_output, torch_output, device):
    if device == "cpu":
        np.testing.assert_allclose(stensor_output.data, torch_output.detach().numpy(), rtol=1e-3)
    elif device == "gpu":
        import cupy as cp
        np.testing.assert_allclose(cp.asnumpy(stensor_output.data), torch_output.detach().numpy(), rtol=1e-3) 
    elif device == "npu":
        np.testing.assert_allclose(stensor_output.data.cpu().detach().numpy(), torch_output.detach().numpy(), rtol=1e-3) 
    else:
        raise ValueError("device must be one of 'cpu', 'gpu' or 'npu'.")
              
                        
def generate_function_testcase(function, torch_function, inputs_args, inputs_stensor_kwargs, inputs_torch_kwargs, torch_backword_input, device):
    inputs_args_stensor = [Tensor(x, requires_grad=True if np.issubdtype(x.dtype, np.floating) else False) if isinstance(x, np.ndarray) else x for x in inputs_args]
    if device == "gpu":
        inputs_args_stensor = [i.to_gpu() if hasattr(i, "data") and isinstance(i.data, np.ndarray) else i for i in inputs_args_stensor]
    elif device == "npu":
        inputs_args_stensor = [i.to_npu() if hasattr(i, "data") and isinstance(i.data, np.ndarray) else i for i in inputs_args_stensor]
        
    out_stensor = function(*inputs_args_stensor, **inputs_stensor_kwargs)

    inputs_args_torch = [torch.tensor(x, requires_grad=True if np.issubdtype(x.dtype, np.floating) else False) if isinstance(x, np.ndarray) else x for x in inputs_args]
    out_torch = torch_function(*inputs_args_torch, **inputs_torch_kwargs)
    print("=================compare forward: =================")
    for input_stensor, input_torch in zip(inputs_args_stensor, inputs_args_torch):
        print("---input_stensor:", input_stensor)
        print("---input_torch:", input_torch)
        if isinstance(input_stensor, Tensor) or isinstance(input_torch, torch.Tensor):
            check_result(input_stensor, input_torch, device)
        else:
            assert input_stensor == input_torch

    
    if isinstance(out_stensor, Tensor) or isinstance(out_torch, torch.Tensor):
        check_result(out_stensor, out_torch, device)
    elif isinstance(out_stensor, tuple) or isinstance(out_torch, tuple):
        assert len(out_stensor) == len(out_torch)
        for out_s, out_t in zip(out_stensor, out_torch):
            print("---out_s:", out_s)
            print("---out_t:", out_t)
            if isinstance(out_s, Tensor) or isinstance(out_t, torch.Tensor):
                check_result(out_s, out_t, device)
            else:
                assert out_s == out_t
    else:
        print("forward output is not a tuple or Tensor.")
        assert out_stensor == out_torch
    
    print("=================compare backward:=================")
    if torch_backword_input != []:
        # Only one tensor output.
        if isinstance(out_stensor, Tensor) and isinstance(out_torch, torch.Tensor):
            out_stensor.backward()
            assert len(torch_backword_input) == 1
            torch_backword_input = [torch.tensor(x) for x in torch_backword_input]
            out_torch.backward(*torch_backword_input)
        # more than one element outputs.
        else:
            for out_s, out_t in zip(out_stensor, out_torch):
                if isinstance(out_s, Tensor) and isinstance(out_t, torch.Tensor):
                    out_stensor[0].backward()
                    torch_backword_input = [torch.tensor(x) for x in torch_backword_input]
                    for ele in torch_backword_input:
                        out_t.backward(ele)

        for input_s, input_t in zip(inputs_args_stensor, inputs_args_torch):
            if input_s is not None and isinstance(input_s, Tensor) and input_s.requires_grad and input_s.grad is not None:
                print("---input_s.grad:", input_s.grad)
                print("---input_t.grad:", input_t.grad)
                check_result(input_s.grad, input_t.grad, device)

                    
test_case_math_ops = [
    {
        "stensor_function": F.add,
        "torch_function": torch.add,
        "inputs": [((2, 3), np.float32), ((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.add,
        "torch_function": torch.add,
        "inputs": [((1,), np.float32), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.add,
        "torch_function": torch.add,
        "inputs": [(1,), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.sub,
        "torch_function": torch.sub,
        "inputs": [((2, 3), np.float32), ((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.sub,
        "torch_function": torch.sub,
        "inputs": [((1,), np.float32), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.sub,
        "torch_function": torch.sub,
        "inputs": [(1,), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.mul,
        "torch_function": torch.mul,
        "inputs": [((2, 3), np.float32), ((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.mul,
        "torch_function": torch.mul,
        "inputs": [((1,), np.float32), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.mul,
        "torch_function": torch.mul,
        "inputs": [(1,), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.div,
        "torch_function": torch.div,
        "inputs": [((2, 3), np.float32), ((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.div,
        "torch_function": torch.div,
        "inputs": [((1,), np.float32), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.div,
        "torch_function": torch.div,
        "inputs": [(1,), ((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.neg,
        "torch_function": torch.neg,
        "inputs": [((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.pow,
        "torch_function": torch.pow,
        "inputs": [((2, 2, 3), np.float32), (2,)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    # {
    #     "stensor_function": F.pow,
    #     "torch_function": torch.pow,
    #     "inputs": [((2, 2, 3), np.float32), (Tensor(2),)],
    #     "inputs_stensor_kwargs":{},
    #     "inputs_torch_kwargs":{},
    #     "torch_backword_input": [((2, 2, 3), np.float32)]
    # },
    {
        "stensor_function": F.sin,
        "torch_function": torch.sin,
        "inputs": [((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.cos,
        "torch_function": torch.cos,
        "inputs": [((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.tan,
        "torch_function": torch.tan,
        "inputs": [((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.exp,
        "torch_function": torch.exp,
        "inputs": [((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.log,
        "torch_function": torch.log,
        "inputs": [((2, 2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.eq,
        "torch_function": torch.eq, 
        "inputs": [((2, 3, 4), np.float32),((2, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.eq,
        "torch_function": torch.eq, 
        "inputs": [((2, 3, 4), np.float32),((1, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.gt,
        "torch_function": torch.gt, 
        "inputs": [((2, 3, 4), np.float32),((2, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.gt,
        "torch_function": torch.gt, 
        "inputs": [((2, 3, 4), np.float32),((1, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.ge,
        "torch_function": torch.ge, 
        "inputs": [((2, 3, 4), np.float32),((2, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.ge,
        "torch_function": torch.ge, 
        "inputs": [((2, 3, 4), np.float32),((1, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.lt,
        "torch_function": torch.lt, 
        "inputs": [((2, 3, 4), np.float32),((2, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.lt,
        "torch_function": torch.lt, 
        "inputs": [((2, 3, 4), np.float32),((1, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
        {
        "stensor_function": F.le,
        "torch_function": torch.le, 
        "inputs": [((2, 3, 4), np.float32),((2, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.le,
        "torch_function": torch.le, 
        "inputs": [((2, 3, 4), np.float32),((1, 3, 4), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": []
    },
    {
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((3, 4), np.float32),((4, 2), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((3, 2), np.float32)]
    },
    {
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((2, 3, 4), np.float32),((4, 2), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3, 2), np.float32)]
    },
    {
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((3, 4), np.float32),((2, 4, 2), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3, 2), np.float32)]
    },
    {
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((2, 3, 4), np.float32),((2, 4, 5), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3, 5), np.float32)]
    },
    {
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((2, 2, 3, 4), np.float32),((2, 4, 2), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3, 2), np.float32)]
    },
    {
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((2, 3, 4), np.float32),((2, 2, 4, 2), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3, 2), np.float32)]
    },
    {
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((2, 2, 3, 4), np.float32),((2, 2, 4, 5), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3, 5), np.float32)]
    },
    {
        # https://github.com/pytorch/pytorch/issues/17678
        # Each operation on float32 has a precision of ~1e-6. 
        # And accumulating a large number of them can lead to big differences.
        # Similar for float64 where it starts around 1e-12 and goes up from there.
        "stensor_function": F.matmul,
        "torch_function": torch.matmul, 
        "inputs": [((1, 4, 511, 511), np.float64),((1, 4, 511, 128), np.float64)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((1, 4, 511, 128), np.float64)]
    },
]

test_case_common_ops = [
    {
        "stensor_function": F.broadcast_to,
        "torch_function": torch.broadcast_to, 
        "inputs": [((1, 3, 4), np.float32),((2, 3, 4),)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3, 4), np.float32)]
    },
    {
        "stensor_function": F.repeat,
        "torch_function": torch.Tensor.repeat, 
        "inputs": [((1, 2, 3), np.float32),((2, 3, 1),)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 6, 3), np.float32)]
    },
    {
        "stensor_function": F.repeat,
        "torch_function": torch.Tensor.repeat, 
        "inputs": [((1, 3, 2, 2), np.float32),((1, 1, 2, 1),)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((1, 3, 4, 2), np.float32)]
    },
    {
        "stensor_function": F.repeat_interleave,
        "torch_function": torch.repeat_interleave, 
        "inputs": [((1, 3, 2, 2), np.float32),((3),),((2,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((1, 3, 6, 2), np.float32)]
    },
    {
        "stensor_function": F.reshape,
        "torch_function": torch.reshape,
        "inputs": [((2, 2, 3), np.float32), ((2, 3, 2),)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3, 2), np.float32)]
    },
    {
        "stensor_function": F.expand_dims,
        "torch_function": torch.Tensor.unsqueeze,
        "inputs": [((2, 3, 4), np.float32), (0,)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((1, 2, 3, 4), np.float32)]
    },
    {
        "stensor_function": F.unsqueeze,
        "torch_function": torch.unsqueeze,
        "inputs": [((2, 3, 4), np.float32), (0,)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((1, 2, 3, 4), np.float32)]
    },
    {
        "stensor_function": F.squeeze,
        "torch_function": torch.squeeze,
        "inputs": [((1, 2, 1, 4), np.float32),],
        "inputs_stensor_kwargs":{"dim":(0)},
        "inputs_torch_kwargs":{"dim":(0)},
        "torch_backword_input": [((2, 1, 4), np.float32)]
    },
    {
        "stensor_function": F.squeeze,
        "torch_function": torch.squeeze,
        "inputs": [((1, 2, 1, 4), np.float32),],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 4), np.float32)]
    },
    {
        "stensor_function": F.flatten,
        "torch_function": torch.flatten, 
        "inputs": [((2, 3, 4), np.float32),],
        "inputs_stensor_kwargs":{"start_dim":1},
        "inputs_torch_kwargs":{"start_dim":1},
        "torch_backword_input": [((2, 12), np.float32)]
    },
    {
        "stensor_function": F.flatten,
        "torch_function": torch.flatten, 
        "inputs": [((2, 3, 4), np.float32),],
        "inputs_stensor_kwargs":{"start_dim":1,"end_dim":-1},
        "inputs_torch_kwargs":{"start_dim":1,"end_dim":-1},
        "torch_backword_input": [((2, 12), np.float32)]
    },
    {
        "stensor_function": F.flatten,
        "torch_function": torch.flatten, 
        "inputs": [((2, 3, 4), np.float32),],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((24,), np.float32)]
    },

    {
        "stensor_function": F.transpose,
        "torch_function": torch.transpose, 
        "inputs": [((2, 3, 4), np.float32),((0,)),((1,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((3, 2, 4), np.float32)]
    },
    {
        "stensor_function": F.masked_fill,
        "torch_function": torch.masked_fill, 
        "inputs": [((1, 2, 3), np.float32),((np.array([[[True, False, True],[False, True, True]]]),)),((1,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((1, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.sum,
        "torch_function": torch.sum, 
        "inputs": [((2, 2, 3, 4), np.float32),((0,)),((True,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((1, 2, 3, 4), np.float32)]
    },
    {
        "stensor_function": F.sum,
        "torch_function": torch.sum, 
        "inputs": [((2, 2, 3, 4), np.float32),((0,)),((False,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3, 4), np.float32)]
    },
    {
        "stensor_function": F.sum,
        "torch_function": torch.sum, 
        "inputs": [((2, 2, 3, 4), np.float32),((-1,)),((True,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3, 1), np.float32)]
    },
    {
        "stensor_function": F.sum,
        "torch_function": torch.sum, 
        "inputs": [((2, 2, 3, 4), np.float32),((-1,)),((False,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3), np.float32)]
    },
    {
        "stensor_function": F.clip,
        "torch_function": torch.clip, 
        "inputs": [((2, 2, 3, 4), np.float32),((0.2,)),((0.8,))],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2, 3, 4), np.float32)]
    },
]

test_case_activation_ops = [
    {
        "stensor_function": F.sigmoid,
        "torch_function": torch.sigmoid, 
        "inputs": [((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.relu,
        "torch_function": torch.relu, 
        "inputs": [((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.leaky_relu,
        "torch_function": torch.nn.functional.leaky_relu, 
        "inputs": [((2, 3), np.float32), (0.2,)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.tanh,
        "torch_function": torch.tanh, 
        "inputs": [((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    #TODO:有概率出错？
    # {
    #     "stensor_function": F.softmax,
    #     "torch_function": torch.softmax, 
    #     "inputs": [((2, 3), np.float32),(-1,)],
    #     "inputs_stensor_kwargs":{},
    #     "inputs_torch_kwargs":{},
    #     "torch_backword_input": [((2, 3), np.float32)]
    # },
    {
        "stensor_function": F.silu,
        "torch_function": torch.nn.functional.silu, 
        "inputs": [((2, 3), np.float32),],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
    {
        "stensor_function": F.swish,
        "torch_function": torch.nn.functional.silu, 
        "inputs": [((2, 3), np.float32),],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 3), np.float32)]
    },
]


test_case_nn_ops = [
    {
        "stensor_function": F.linear,
        "torch_function": torch.nn.functional.linear, 
        "inputs": [((2, 3), np.float32), ((2, 3), np.float32)],
        "inputs_stensor_kwargs":{},
        "inputs_torch_kwargs":{},
        "torch_backword_input": [((2, 2), np.float32)]
    },

]

test_case_lists = [test_case_math_ops, test_case_common_ops, test_case_activation_ops, test_case_nn_ops]

test_cases = functools.reduce(lambda x, y: x + y, test_case_lists)

def _exec_inner(device):
    for case in test_cases:
        stensor_function = case["stensor_function"]
        torch_function = case["torch_function"]
        print("########################## start to execute stensor function test: ", str(stensor_function), \
              "execute torch function test: ", str(torch_function), " ##########################")
        inputs = case["inputs"]
        inputs_numpy = [np.random.normal(0.0, 1.0,(i[0])).astype(i[1]) if isinstance(i[0], tuple) and len(i) == 2 else i[0] for i in inputs]
        if stensor_function == F.softmax:
            inputs_numpy = [np.random.rand(*i[0]).astype(i[1]) if isinstance(i[0], tuple) and len(i) == 2 else i[0] for i in inputs]
        inputs_numpy = [np.abs(i) + 1 if stensor_function == F.log else i for i in inputs_numpy]
  
        inputs_stensor_kwargs = case["inputs_stensor_kwargs"]
        inputs_torch_kwargs = case["inputs_torch_kwargs"]
        torch_backword_input = case["torch_backword_input"]
        torch_backword_input = [np.ones(i[0]).astype(i[1]) for i in torch_backword_input]   
        generate_function_testcase(stensor_function, torch_function, inputs_numpy, inputs_stensor_kwargs, inputs_torch_kwargs, \
                                    torch_backword_input, device)


@pytest.mark.parametrize("recomputer", [True, False])
def test_exec(recomputer):
    Config.recomputer = recomputer
    print("recomputer: ", recomputer)
    Config.device = "cpu"
    _exec_inner("cpu")
    if Config.gpu_enable:
        Config.device = "gpu"
        _exec_inner("gpu")
    if Config.npu_enable:
        Config.device = "npu"
        _exec_inner("npu")

def test_function_max1():
    x = np.random.rand(2, 3, 4)
    x_s = Tensor(x, requires_grad=True)
    x_t = torch.tensor(x, requires_grad=True)
    value_s, indences_s = F.max(x_s, 0, False)
    value_t, indences_t = torch.max(x_t, 0, False)
    assert np.allclose(value_s.data, value_t.detach().numpy()), f"max test failed"
    assert np.allclose(indences_s.data, indences_t.detach().numpy()), f"max test failed" 

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((3, 4)))))

    assert np.allclose(x_s.grad.data, x_t.grad.numpy()), f"max test backward failed"

    # indences_s.backward()
    # indences_t.backward(torch.tensor(np.ones((3, 4))))
    # assert np.allclose(x_s.grad.data, x_t.grad.numpy()), f"max test backward failed"

def test_function_max2():
    x = np.random.rand(2, 3, 4)
    x_s = Tensor(x, requires_grad=True)
    x_t = torch.tensor(x, requires_grad=True)
    value_s, indences_s = F.max(x_s, -1, True)
    value_t, indences_t = torch.max(x_t, -1, True)
    assert np.allclose(value_s.data, value_t.detach().numpy()), f"max test failed"
    assert np.allclose(indences_s.data, indences_t.detach().numpy()), f"max test failed" 

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((2, 3, 1)))))
    assert np.allclose(x_s.grad.data, x_t.grad.numpy()), f"max test backward failed"


def test_function_min():
    x = np.random.rand(2, 3, 4)
    x_s = Tensor(x, requires_grad=True)
    x_t = torch.tensor(x, requires_grad=True)
    value_s, indences_s = F.min(x_s, 0, False)
    value_t, indences_t = torch.min(x_t, 0, False)
    assert np.allclose(value_s.data, value_t.detach().numpy()), f"min test failed"
    assert np.allclose(indences_s.data, indences_t.detach().numpy()), f"min test failed" 

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((3, 4)))))
    assert np.allclose(x_s.grad.data, x_t.grad.numpy()), f"min test backward failed"


def test_function_getitem1():
    x = np.random.rand(2, 3, 4)
    x_s = Tensor(x, requires_grad=True)
    x_t = torch.tensor(x, requires_grad=True)
    value_s = F.get_item(x_s, 0)
    value_t = x_t[0]
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((3, 4)))))
    assert np.allclose(x_s.grad.data, x_t.grad.numpy())


def test_function_getitem2():
    x = np.random.rand(2, 3, 4)
    x_s = Tensor(x, requires_grad=True)
    x_t = torch.tensor(x, requires_grad=True)

    flat_ids = Tensor(np.array([1, 2, 3]))       #[8, 128] -> [8*128,]

    #value_s = F.get_item(x_s, (slice(0,1,1),slice(0,1,1),slice(0,2,1)))
    value_s = x_s[0:1:1, 0:1:1, 0:2:1]
    value_t = x_t[0:1:1, 0:1:1, 0:2:1]
    print(value_s.shape)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((1, 1, 2)))))
    print(x_s.grad)
    print(x_t.grad)
    assert np.allclose(x_s.grad.data, x_t.grad.numpy())


def test_function_softmax():
    x = np.random.rand(2, 3)
    x_s = Tensor(x, requires_grad=True)
    x_t = torch.tensor(x, requires_grad=True)      #[8, 128] -> [8*128,]

    value_s = F.softmax(x_s, -1)
    value_t = torch.nn.Softmax(-1)(x_t)
    value_t = torch.softmax(x_t, -1)
    print(value_s)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((2,3)))))
    print(x_s.grad)
    print(x_t.grad)
    assert np.allclose(x_s.grad.data, x_t.grad.numpy())


def test_function_concat():
    x1 = np.random.rand(2, 3)
    x2 = np.random.rand(2, 3)
    x_s1 = Tensor(x1, requires_grad=True)
    x_t1 = torch.tensor(x1, requires_grad=True)      #[8, 128] -> [8*128,]
    x_s2 = Tensor(x2, requires_grad=True)
    x_t2 = torch.tensor(x2, requires_grad=True) 

    value_s = F.concat((x_s1, x_s2), axis=-1)
    value_t = torch.cat((x_t1, x_t2), -1)
    print(value_s)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((2,6)))))
    print(x_s1.grad)
    print(x_t1.grad)
    assert np.allclose(x_s1.grad.data, x_t1.grad.numpy())
    print(x_s2.grad)
    print(x_t2.grad)
    assert np.allclose(x_s2.grad.data, x_t2.grad.numpy())

#TODO
def test_function_dropout():
    from stensor import Config
    Config.train = True
    x = np.random.rand(2, 3)
    x_s = Tensor(x, requires_grad=True)
    x_t = torch.tensor(x, requires_grad=True)      #[8, 128] -> [8*128,]

    value_s = F.dropout(x_s, 0.)
    value_t = torch.dropout(x_t, 0., train=True)
    print(value_s)
    print(value_t)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.tensor((np.ones((2,3)))))
    print(x_s.grad)
    print(x_t.grad)
    assert np.allclose(x_s.grad.data, x_t.grad.numpy())


@pytest.mark.parametrize("reduction", ['sum', 'mean', 'none'])
def test_function_softmax_cross_entropy(reduction):
    seed = 1234
    np.random.seed(seed)
    torch.manual_seed(seed)

    input = torch.randn(3, 5, requires_grad=True)
    target = torch.empty(3, dtype=torch.long).random_(5)
    input_s = Tensor(input.detach().numpy())
    target_s = Tensor(target.detach().numpy())
    
    
    value_t = torch.nn.CrossEntropyLoss(reduction=reduction)(input, target)
    value_s = nn.SoftmaxCrossEntropy(reduction=reduction)(input_s, target_s)

    print(value_s)
    print(value_t)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    if reduction=='none':
        value_t.backward(torch.tensor((np.ones((3,)))))
    else:
        value_t.backward()
    print(input.grad)
    print(input_s.grad)
    assert np.allclose(input_s.grad.data, input.grad.numpy())


def test_function_rmsnorm():
    seed = 1234
    np.random.seed(seed)
    torch.manual_seed(seed)

    class RMSNorm(torch.nn.Module):
        def __init__(self, dim: int, eps: float):
            super().__init__()
            self.eps = eps
            self.weight = torch.nn.Parameter(torch.ones(dim))

        def _norm(self, x):
            #return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
            return x / torch.sqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        
        def forward(self, x):
            output = self._norm(x.float()).type_as(x)
            return output * self.weight


    input = torch.randn(1, 511, 512, requires_grad=True)
    input_s = Tensor(input.detach().numpy())

    t_rms = RMSNorm(512, eps=1e-5)
    s_rms = nn.RMSNorm(512, eps=1e-5)
    value_t = t_rms(input)
    value_s = s_rms(input_s)

    print(value_s)
    print(value_t)

    print("================================")
    value_s.backward()
    value_t.backward(torch.tensor((np.ones((1, 511, 512)))))
    
    print(s_rms.gamma.grad.shape)
    print(t_rms.weight.grad.shape)
    np.testing.assert_allclose(s_rms.gamma.grad.data, t_rms.weight.grad.detach().numpy(), rtol=1e-4) 
    
    print(input.grad)
    print(input_s.grad)

    assert np.allclose(input_s.grad.data, input.grad.numpy())


def test_function_view_as_complex():
    seed = 1234
    np.random.seed(seed)
    torch.manual_seed(seed)

    input = torch.randn((1, 4, 2, 2, 2), dtype=torch.float64, requires_grad=True)
    input_s = Tensor(input.detach().numpy())
    def to_complex(x):
        real_part = x[..., 0]  # 取最后一个维度的第一个部分，实部
        imag_part = x[..., 1]  # 取最后一个维度的第二个部分，虚部

        # Step 2: 合并为复数张量
        complex_x = F.to_complex(real_part, imag_part)
        #complex_x = real_part + 1j * imag_part
        return complex_x

    
    value_t = torch.view_as_complex(input)
    value_s = to_complex(input_s)

    print(value_s)
    print(value_t)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.ones((1, 4, 2, 2), dtype=torch.complex64))
    print(input.grad)
    print(input_s.grad)
    assert np.allclose(input_s.grad.data, input.grad.numpy())


def test_function_view_as_real():
    seed = 1234
    np.random.seed(seed)
    torch.manual_seed(seed)

    input = torch.randn((1, 4, 2, 2), dtype=torch.complex64, requires_grad=True)
    input_s = Tensor(input.detach().numpy())
    
    
    value_t = torch.view_as_real(input)
    value_s = F.to_real(input_s)

    print(value_s)
    print(value_t)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.ones(1, 4, 2, 2, 2))
    print(input.grad)
    print(input_s.grad)
    assert np.allclose(input_s.grad.data, input.grad.numpy())


def test_function_mul_complex():
    seed = 1234
    np.random.seed(seed)
    torch.manual_seed(seed)

    input1 = torch.randn((1, 4, 2, 2), dtype=torch.complex64, requires_grad=True)
    input2 = torch.randn((1, 4, 1, 2), dtype=torch.complex64, requires_grad=True)
    input_s1 = Tensor(input1.detach().numpy())
    input_s2 = Tensor(input2.detach().numpy())
    
    value_t = input1 * input2
    value_s = input_s1 * input_s2

    print(value_s)
    print(value_t)
    assert np.allclose(value_s.data, value_t.detach().numpy())

    value_s.backward()
    value_t.backward(torch.ones(1, 4, 2, 2).type_as(input1))
    print(input1.grad)
    print(input_s1.grad)

    np.testing.assert_allclose(input_s1.grad.data, input1.grad.detach().numpy(), rtol=1e-4) 

def numerical_diff(f, *input_x, eps=1e-4):
    res = []
    for i in range(len(input_x)):
        input_x_add_eps = []
        input_x_sub_eps = []
        for j, ele in enumerate(input_x):
            if i == j and isinstance(ele, Tensor):
                x0 = Tensor(ele.data - eps)
                input_x_sub_eps.append(x0)
                x1 = Tensor(ele.data + eps)
                input_x_add_eps.append(x1)
                print("add x0: ",x0)
                print("add x1: ",x1)
            else:
                input_x_sub_eps.append(ele)
                input_x_add_eps.append(ele)
                print("add other input ele: ",ele)

        y0 = f(*input_x_sub_eps)
        y1 = f(*input_x_add_eps)
       
        out = (y1.data - y0.data) / (2 * eps)
        res.append(out)
        print("numerical_grad: ", out)
        print(type(out))
    return res