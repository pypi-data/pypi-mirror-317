"""Registry the relation."""

from collections import UserDict


class Registry(UserDict):
    """Registry class for registry functions for tensor call primitive ops function."""

    def register(self, obj_str, obj):
        if isinstance(obj_str, str):
            self[obj_str] = obj

    def get(self, obj_str):
        """Get the value by str."""
        if not isinstance(obj_str, str):
            raise TypeError("key for tensor registry must be string.")
        return self[obj_str]


tensor_operator_registry = Registry()
