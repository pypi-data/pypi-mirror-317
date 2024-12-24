import collections
import functools
import inspect

from typing import _GenericAlias, get_args, get_origin


def para_check(func):
    """
    Check the inputs type of operation which is decorated by function annotations.
    The support types are Tensor, Number, List, tuple and theirs only one-layer nested structure, such as tuple[Number], tuple[Tensos].
    So the annotations of the parameter is similar to the structure of Tensor, list[int] or Union(Tuple[int], Tuple[Tensor]).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, 'has_checked'):
            wrapper.has_checked = True 
        
            func_name = func.__name__
            msg = "For '{func_name}', The {arbitrary_argument}: '{name}' must be {expected!r}, but got {got!r}, value: {value!r}."

            # 获取函数定义的参数
            sig = inspect.signature(func)
            parameters = sig.parameters  # 参数有序字典
            arg_keys = tuple(parameters.keys())  # 参数名称        
            CheckItem = collections.namedtuple('CheckItem', ('arbitrary_argument','name', 'annotation', 'value'))
            check_list = []

            # The annotation is instance of typing._GenericAlias, get the real instance by __args__.
            # collect args   *args 传入的参数以及对应的函数参数注解
            for i, value in enumerate(args):
                name = arg_keys[i]
                anno = parameters[name].annotation

                check_list.append(CheckItem("variable positional arguments", name, anno, value))
                # Handle with one-layer nested structure.
                # if isinstance(value, (list, tuple)):
                #     for ele in value:
                #        check_list.append(CheckItem("variable positional arguments", name, anno, value)) 

            # collect kwargs  **kwargs 传入的参数以及对应的函数参数注解
            for name, value in kwargs.items():
                anno = parameters[name].annotation
                check_list.append(CheckItem("keyword arguments", name, anno, value))

            # check type
            for item in check_list:
                # Handle with Union(Tuple[int], Tuple[Tensor]).
                if isinstance(item.annotation, _GenericAlias): # Union[]
                    # get the real instance by __args__.
                    for ele in item.annotation.__args__:
                        if not isinstance(item.value, item.annotation.__args__):
                            error = msg.format(func_name=func_name, arbitrary_argument=item.arbitrary_argument, name=item.name, expected=item.annotation.__args__, 
                                            got=type(item.value), value=item.value)
                            raise TypeError(error)
                else:
                    # Handle with Tensor, Number, List, tuple.
                    if not is_generic_type(item.annotation):
                        if not isinstance(item.value, item.annotation):
                            error = msg.format(func_name=func_name, arbitrary_argument=item.arbitrary_argument, name=item.name, expected=item.annotation, 
                                            got=type(item.value), value=item.value)
                            raise TypeError(error)
                    # Handle with List[Tensor].
                    else:
                        origin_type = get_origin(item.annotation)
                        args_type = get_args(item.annotation)
                        if not isinstance(item.value, origin_type) and isinstance(item.value, args_type):
                            error = msg.format(func_name=func_name, arbitrary_argument=item.arbitrary_argument, name=item.name, expected=f"{origin_type} of {args_type}", 
                                            got=f"{type(item.value)}", value=item.value)
                            raise TypeError(error)
                
        return func(*args, **kwargs)
    return wrapper


def is_generic_type(tp):
    # 使用 get_origin 获取原始类型
    origin = get_origin(tp)
    args_type = get_args(tp)
    return origin is not None and args_type is not None
