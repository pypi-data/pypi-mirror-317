import contextlib


class Config:
    gpu_enable = False
    npu_enable = False
    device = "cpu"
    enable_backprop = True
    train = True
    recomputer = False
    debug = False


@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)
    setattr(Config, name, value)
    try:
        yield
    finally:
        setattr(Config, name, old_value)


def no_grad():
    return using_config('enable_backprop', False)

def recomputer():
    return using_config('recomputer', True)

def test_mode():
    return using_config('train', False)


__all__ = ['Config', 'no_grad', 'recomputer']
