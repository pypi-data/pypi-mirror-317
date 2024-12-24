# from stensor import Tensor, Sin, Cos
# import sys, os
# stensor_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# sys.path.append(stensor_dir)
# print("sys.path: ",sys.path)
import numpy as np
import cupy as cp
import time
import torch
from stensor.ops import functional as F
from stensor import Tensor, Config


def _torch_count(*args):
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    for i in range(100):
        args = [x.to(device) for x in args]
        torch_forward_count, torch_backward_count = 0, 0
        backward_input = torch.ones(64, 1024, 1024).to(device)
        memory_before = torch.cuda.memory_allocated()
        time0 = time.time()
        y = torch.add(*args)
        time1 = time.time()
        y.backward(backward_input)
        time2 = time.time()
        step_forward_time = time1-time0
        step_backward_time = time2-time1
        #warm up
        if i > 10:
            torch_forward_count += step_forward_time
            torch_backward_count += step_backward_time
            
        if i == 10:
            memory_after = torch.cuda.memory_allocated()
            memory_used_by_matmul = memory_after - memory_before
            print(f"torch Memory used by matmul: {memory_used_by_matmul} bytes")
            
    print(f"torch average forward step time: {torch_forward_count/90:.6f}, backward step time: {torch_backward_count/90:.6f}")


def _cp_function_count(*args):
    cp_count = 0
    time0 = time.time()
    for i in range(100):
        time0 = time.time()   
        y = cp.add(*args)
        time1 = time.time()
        step_time = time1-time0

        if i > 10:
            cp_count += step_time
    print(f"cp average step time: {cp_count/90:.6f}" )


def _stensor_function_count(*args):
    #Config.debug = True
    stensor_forward_count, stensor_backward_count = 0, 0
    time0 = time.time()
    for i in range(100):
        mempool = cp.get_default_memory_pool()
        memory_before = mempool.used_bytes()
        time0 = time.time()   
        y = F.add(*args)
        time1 = time.time()
        y.backward()
        time2 = time.time()
        step_forward_time = time1-time0
        step_backward_time = time2-time1
        
        #warm up
        if i > 10:
            stensor_forward_count += step_forward_time
            stensor_backward_count += step_backward_time
            
        if i == 10:
            memory_after = mempool.used_bytes()
            memory_used_by_matmul = memory_after - memory_before
            print(f"stensor Memory used by matmul: {memory_used_by_matmul} bytes")
            
    print(f"stensor average forward step time: {stensor_forward_count/90:.6f}, backward step time: {stensor_backward_count/90:.6f}")


def test_exec():
    if not Config.gpu_enable:
        return
    print("=======start test =====")
    Config.device = "gpu"
    print("=======shape: (64, 1024, 1024)=========")
    x_0 = np.random.rand(64, 1024, 1024).astype(np.float32)
    x_1 = np.random.rand(64, 1024, 1024).astype(np.float32)
    np_input = [x_0, x_1]
    torch_input = [torch.tensor(i, dtype=torch.float32, requires_grad=True) for i in np_input]
    cp_input = [cp.asarray(i).astype(cp.float32) for i in np_input]
    stensor_input = [Tensor(i) for i in cp_input]
    _torch_count(*torch_input)
    _cp_function_count(*cp_input)
    _stensor_function_count(*stensor_input)
