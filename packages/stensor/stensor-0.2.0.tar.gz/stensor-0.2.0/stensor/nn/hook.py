from stensor import nn, Tensor
import stensor.ops.functional as F

iteration = 0


def forward_print_hook(name):  # print data type, shape, norm of inputs and output of forward 
    def print_tatistics_and_dtype_hooks(module, inputs, output):
        global iteration
        if 0 <= iteration:
            # 打印层的名称和输出数据的dtype
            if isinstance(inputs, tuple):
                for ind, value in enumerate(inputs):
                    if value is None:
                        print(f"inputs, {name}, index={ind}, None")
                    elif isinstance(value, Tensor):
                        print(
                            f"inputs, {name}, index={ind}, DataType:{inputs[ind].dtype}, Shape:{inputs[ind].shape}, "
                            f"Norm:{inputs[ind].float().norm().item} "
                            f"mean: {F.mean(inputs[ind].float()).item} min: {F.min(inputs[ind].float())[0].item} "
                            f"max: {F.max(inputs[ind].float())[0].item}")
            elif isinstance(inputs, Tensor):
                print(
                    f"input0, {name}, DataType: {inputs.dtype}, Shape:{inputs.shape}, Norm:{inputs.norm().item} "
                    f"mean: {F.mean(inputs.float()).item} min: {F.min(inputs.float())[0].item} max: {F.max(inputs.float())[0].item}")

            if isinstance(output, tuple):
                for ind, value in enumerate(output):
                    if value is None:
                        print(f"output, {name}, index={ind}, None")
                    elif isinstance(value, Tensor):
                        print(
                            f"output, {name}, index={ind}, DataType:{output[ind].dtype}, Shape:{output[ind].shape}, "
                            f"Norm:{output[ind].float().norm().item} "
                            f"mean: {F.mean(output[ind].float()).item} "
                            f"min: {F.min(output[ind].float())[0].item} max: {F.max(output[ind].float())[0].item}")
            elif isinstance(output, Tensor):
                try:
                    print(
                        f"output0, {name}, DataType:{output.dtype}, "
                        f"Shape:{output.shape}, Norm:{output.norm().item} "
                        f"mean: {F.mean(output.float()).item} min: {F.min(output.float())[0].item} max: {F.max(output.float())[0].item}")
                except Exception as e:
                    print(e)
    return print_tatistics_and_dtype_hooks


def backward_print_hook(name):  # print datatype, shape, norm of input and output of backward  
    def print_tatistics_and_dtype_hooks(module, grad_input, grad_output):
        global iteration
        if 0 <= iteration:
            # 打印层的名称和输出数据的dtype
            if isinstance(grad_input, (list, tuple)):
                for ind, value in enumerate(grad_input):
                    if value.data is None:
                        print(f"grad_input, {name}, index={ind}, None")
                    elif isinstance(value, Tensor):
                        print(
                            f"grad_input, {name}, index={ind}, DataType:{grad_input[ind].dtype}, "
                            f"Shape:{grad_input[ind].shape}, Norm:{grad_input[ind].norm().item} "
                            f"mean: {F.mean(grad_input[ind]).item} min: {F.min(grad_input[ind])[0].item} "
                            f"max: {F.max(grad_input[ind])[0].item}")
            elif isinstance(grad_input, Tensor):
                print(
                    f"grad_input0, {name}, DataType:{grad_input.dtype}, "
                    f"Shape:{grad_input.shape}, Norm:{grad_input.norm().item} "
                    f"mean: {F.mean(grad_input).item} min: {F.min(grad_input)[0].item} max: {F.max(grad_input)[0].item}")
 
            if isinstance(grad_output, (list, tuple)):
                for ind, value in enumerate(grad_output):
                    if value.data is None:
                        print(f"grad_output, {name}, index={ind}, None")
                    elif isinstance(value, Tensor):
                        print(
                            f"grad_output, {name}, index={ind}, DataType:{grad_output[ind].dtype}, "
                            f"Shape:{grad_output[ind].shape}, Grad_Norm:{grad_output[ind].norm().item} "
                            f"mean: {F.mean(grad_output[ind]).item} min: {F.min(grad_output[ind])[0].item} "
                            f"max: {F.max(grad_output[ind])[0].item}")
            elif isinstance(grad_output, Tensor):
                print(
                    f"grad_output0, {name}, DataType:{grad_output.dtype}, Shape:{grad_output.shape}, "
                    f"Norm:{grad_output.norm().item} "
                    f"mean: {F.mean(grad_output).item} min: {F.min(grad_output)[0].item} max: {F.max(grad_output)[0].item}")
    return print_tatistics_and_dtype_hooks


def register_print_hooks(model):
    for name, module in model.names_and_submodules():
        # 过滤掉不需要的模块
            if isinstance(module, (nn.Module)):  # 根据需要调整条件
                print_forward_hook = forward_print_hook(name)
                print_backward_hook = backward_print_hook(name)
                module.register_forward_hook(print_forward_hook)
                module.register_backward_hook(print_backward_hook)


__all__=["register_print_hooks",]