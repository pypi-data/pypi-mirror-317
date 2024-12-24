"""Registry the operation implementation and Select operation."""
from collections import UserDict
from stensor.config import Config


class OperatorDispatcher(UserDict):
    """Registry class for registry kernel for functions call primitive ops function."""
    def register(self, obj_str, obj):
        self[obj_str] = obj

operator_dispatcher = OperatorDispatcher()


def get_operator_impl(op_name, device, *args):
    key = (op_name, device)
    impl = operator_dispatcher.get(key, None)
    if impl is None:  
        #print(f"get operator {key} implementation falied, choose cpu implementation.")
        impl = operator_dispatcher.get((op_name, Config.device))

    args = impl._transfer_tensor_args(args)
    return impl(*args)
