import os
import subprocess


def pair(x):
    if isinstance(x, int):
        return (x, x)
    elif isinstance(x, tuple):
        assert len(x) == 2
        return x
    else:
        raise ValueError


def _dot_var(v, verbose=False):
    dot_var = '{} [label="{}", color=orange, style=filled]\n'

    name = '' if v.name is None else v.name
    if verbose and v.data is not None:
        if v.name is not None:
            name += ': '
        if hasattr(v, "shape"):
            name += str(v.shape) + ' ' + str(v.dtype)

    return dot_var.format(id(v), name)


def _dot_func(f):
    '''
    在 Graphviz 中，style 属性可以有以下几个值：
    filled：这是默认值，意味着节点的背景颜色会填充整个节点区域。
    dashed：节点的边框是虚线。
    dotted：节点的边框是点线。
    solid：节点的边框是实线（与默认值相同）。
    invis：节点是不可见的，但仍然占据空间。
    '''
    # for function
    dot_func = '{} [label="{}", color=lightblue, style=filled, shape=box]\n'
    ret = dot_func.format(id(f), f.name)

    # for edge
    dot_edge = '{} -> {}\n'
    for x in f.inputs:
        ret += dot_edge.format(id(x), id(f))
    for y in f.outputs:  # y is weakref
        ret += dot_edge.format(id(f), id(y()))
    return ret


def get_dot_graph(outputs, verbose=True):
    """Generates a graphviz DOT text of a computational graph.

    Build a graph of functions and variables backward-reachable from the
    output. To visualize a graphviz DOT text, you need the dot binary from the
    graphviz package (www.graphviz.org).

    Args:
        output (dezero.Variable): Output variable from which the graph is
            constructed.
        verbose (bool): If True the dot graph contains additional information
            such as shapes and dtypes.

    Returns:
        str: A graphviz DOT text consisting of nodes and edges that are
            backward-reachable from the output
    """
    txt = ''
    funcs = []
    seen_set = set()

    def add_func(f):
        if f not in seen_set:
            funcs.append(f)
            # funcs.sort(key=lambda x: x.generation)
            seen_set.add(f)

    add_func(outputs.creator)
    txt += _dot_var(outputs, verbose)

    while funcs:
        func = funcs.pop()
        txt += _dot_func(func)
        for x in func.inputs:
            txt += _dot_var(x(), verbose)

            if x().creator is not None:
                add_func(x().creator)

    return 'digraph g {\n' + txt + '}'


def plot_dot_graph(outputs, file_dir="./graph", file_name="model", verbose=True):
    dot_graph = get_dot_graph(outputs, verbose)

    #current_directory = os.path.dirname(os.path.abspath(__file__))
    #tmp_dir = os.path.join(current_directory, './graph')

    to_file_dot = file_name + '.dot'
    to_file_png = file_name + '.png'

    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    graph_path = os.path.join(file_dir, to_file_dot)

    with open(graph_path, 'w') as f:
        f.write(dot_graph)

    to_file = os.path.join(file_dir, to_file_png)
    extension = os.path.splitext(to_file)[1][1:]  # Extension(e.g. png, pdf)
    cmd = 'dot {} -T {} -o {}'.format(graph_path, extension, to_file)
    subprocess.run(cmd, shell=True)

    # Return the image as a Jupyter Image object, to be displayed in-line.
    try:
        from IPython import display
        return display.Image(filename=to_file)
    except:
        pass
