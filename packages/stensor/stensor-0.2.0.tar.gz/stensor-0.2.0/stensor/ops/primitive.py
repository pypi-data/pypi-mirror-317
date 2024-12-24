import weakref

from stensor.common import Tensor
from stensor import Config
from stensor.ops.kernel.dispatcher import get_operator_impl


class Primitive:
    def __init__(self, name, *args):
        self.name = name
        self.args = args
        self.device = None

    def __call__(self, *inputs_data):
        # Make sure that all operations' inputs is Tensor.
        inputs = []
        for x in inputs_data:
            if isinstance(x, Tensor):
                self.device = x.device
                inputs.append(x)
            else:
                inputs.append(Tensor(x))
        #inputs = [x if isinstance(x, Tensor) else Tensor(x) for x in inputs]
        
        # Pull the real data to compute.
        xs = [x.data for x in inputs]
        ys = self.forward(xs)  # Single op execution
        if not isinstance(ys, tuple):
            ys = (ys,)
        outputs = [Tensor(y, device=self.device) for y in ys]

        if Config.enable_backprop and inputs:
            self.generation = max([x.generation for x in inputs])
            for output in outputs:
                output.set_creator(self)
            self.inputs = [weakref.ref(x) for x in inputs]
            self.outputs = [weakref.ref(y) for y in outputs]
            self.save_inputs = inputs

        return outputs if len(outputs) > 1 else outputs[0]

    def forward(self, xs):
        impl_instance = get_operator_impl(self.name, self.device, *self.args)
        impl_instance.name = self.name
        if not Config.recomputer:
            self.impl_instance = impl_instance
        impl_instance._check_inputs_status(xs)
        return impl_instance.forward_outer(*xs)

    def backward(self, gys):
        if not Config.recomputer:
            impl_instance = self.impl_instance
        else:
            impl_instance = get_operator_impl(self.name, self.device, *self.args)
            impl_instance.name = self.name
        impl_instance.inputs = self.inputs
        impl_instance.outputs = self.outputs
        impl_instance._check_inputs_status(gys)
        return impl_instance.backward_outer(*gys)


__all__=["Primitive"]
