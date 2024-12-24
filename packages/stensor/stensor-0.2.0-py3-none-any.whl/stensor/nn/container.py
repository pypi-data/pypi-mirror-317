from stensor.nn.module import Module


class Sequential(Module):
    def __init__(self, *layers):
        super().__init__()
        self.layers = []
        for i, layer in enumerate(layers):
            setattr(self, 'l' + str(i), layer)
            self.layers.append(layer)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x


class ModuleList(Module):
    def __init__(self, modules=None):
        super().__init__()
        if modules is not None:
            for idx, module in enumerate(modules):
                self._submodules[str(idx)] = module

    def __bool__(self):
        return len(self._submodules) != 0

    def __len__(self):
        return len(self._submodules)

    def __iter__(self):
        return iter(self._submodules.values())
    
    def extend(self, submodules):
        """
        Appends submodules from a Python iterable to the end of the list.

        Args:
            submodules(list): The submodules to be extended, the types of submodules can not be submoduleDict.

        Raises:
            TypeError: If the argument submodules are not a list of submodules.
        """
        cls_name = self.__class__.__name__
        if not isinstance(submodules, list):
            raise TypeError(f"For '{cls_name}', the new submodules wanted to append "
                            f"should be instance of list, but got {type(submodules).__name__}.")
        #prefix, _ = _get_prefix_and_index(self._submodules)
        for submodule in submodules:
            if self._auto_prefix:
                submodule.update_parameters_name(str(len(self)) + ".")
            self._submodules[str(len(self))] = submodule
        return self

    def append(self, submodule):
        """
        Appends a given submodule to the end of the list.

        Args:
            submodule(submodule): The submodule to be appended.
        """
        if self._valid_submodule(submodule, self.__class__.__name__):
            # if self._auto_prefix:
            #     prefix, _ = _get_prefix_and_index(self._submodules)
            #     submodule.update_parameters_name(prefix + str(len(self)) + ".")
            self._submodules[str(len(self))] = submodule

    def _valid_submodule(self, submodule, op_name=None):
        """Internal function, used to check whether the input submodule is a subclass of submodule."""
        if issubclass(submodule.__class__, Module):
            return True
        msg_prefix = f"For '{op_name}'," if op_name else ""
        raise TypeError(f'{msg_prefix} each submodule must be subclass of submodule, but got {type(submodule).__name__}.')
    
    def forward(self, *inputs):
        raise NotImplementedError


__all__=["Sequential", "ModuleList"]
