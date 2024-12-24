- [stensor介绍](#stensore介绍)
- [快速入门](#快速入门)
    - [目录层级](#目录层级)
        - [common模块](#common模块)
        - [dataset模块](#dataset模块)
        - [nn模块](#nn模块)
        - [ops模块](#ops模块)
- [TODOList](#TODOList) 
- [展望](#展望)    
    - [动静统一](#动静统一)
    - [元模块模版](#元模块模版)
  

# stensor介绍

stensor是一种轻量化的深度学习训练/推理框架，对标pytorch提供的接口。

主要特性包括：

    - 自动微分

    - 算子入参类型校验

    - tensor接口注册机制


# 快速入门

参考test_transfomer实现翻译任务，主要包括以下流程：

    1. 设置超参数
      1）.arg = ArgConfig()
    2. 读取数据 
      1）.创建Dateset 
      2）.Dataset传递给DataLoader 
    3. 创建模型
      1）.模型初始化 model = Model(arg) 
    4. 创建优化器
      1）.优化器初始化 opt = Optimizer(arg_opt, model.parameters())
    5. 训练
      1）.DataLoader迭代产生训练数据提供给模型
      2）.模型计算 y = model(x) 
      3）.损失函数计算 loss = loss_f(y, target) 
      4）.反向传播 loss.backward() 
      5）.优化器更新参数 opt.update()      
    6. 推理


## 目录层级

- `model/` —— 模型库
- `stensor/` —— 源代码目录
  - `common/` —— tensor类
  - `dataset/` —— datase  - `common/` —— tensor类定义
  - `dataset/` —— dataload类
  - `nn/` —— nn部分代码
  - `ops/` —— 算子库
  - `__init__.py` —— 暴露的所有api接口
  - `config.py` —— 上下文环境管理
- `tests/` —— 测试用例
- `requirements.txt` —— 依赖的三方库
- `README.md` —— 当前文件
- `LICENSE` —— 许可证文件
- `.gitignore` —— Git忽略文件列表

### common模块

- `common/` —— 源代码目录
  - `__init__.py` —— 暴露接口
  - `_register_for_tensor.py` —— 在functional.py中注册tensor接口
  - `tensor.py` —— Tensor类
  - `utils.py` —— 工具函数

Tensor类的设计思路：

    1. Tensor类属性self.data中承载真实数据。

    2. 以loss的输出Tensor开始，调用backward接口进行自动微分流程。

Parameter类的设计思路：

    1. 继承自Tensor类，定义为模型层中的权重参数。以属性self.required_grad来判断是否进行权重更新。


### dataset模块

- `common/` —— 源代码目录
  - `__init__.py` —— 暴露接口
  - `dataloaders.py` —— Dataset负责建立索引到样本的映射
  - `datasets.py` —— DataLoader负责以特定的方式从数据集中迭代的产生 一个个batch的样本集合
 —— 源代码目录
  - `layer/` —— 所有nn层接口 
    - `__init__.py` —— 暴露接口
    - `activation.py` —— 激活函数层
    - `convolution.py` —— 卷积层
    - `embedding.py` —— 编码层
    - `linear.py` —— 线性层
    - `normalization.py` —— 正则化层
    - `pooling.py` —— 池化层
    - `rnn.py` —— RNN层
  - `loss/` —— 损失函数层
    - `__init__.py` —— 暴露接口
    - `loss.py` —— 损失函数层，通常作为独立的一层与模型组合
  - `opt/` —— 优化器
    - `__init__.py` —— 暴露接口
    - `optimizer.py` —— 优化器更新参数
  - `__init__.py` —— 暴露接口
  - `container.py` —— module的容器类
  - `metric.py` —— 评测指标
  - `module.py` —— 模型构建的基本单元
  - `utils.py` —— 工具函数

Module类的设计思路：

    1.'__init__'和forward两个函数进行模型的初始化和正向计算过程的搭建。
    
    2.用_params储存所有的参数。用_submodules储存所有的子模块。通过重载__setattr__魔术方法，在构建model时，自动将当前module的parameter和submodule存储，最终树状结构通过names_and_parameters和names_and_submodules两个接口使用yield打印出来。

    3.to_gpu和to_cpu接口分别将params转化为numpy/cupy的格式。

    4.load_weights和load_weights接口将numpy格式的params保存和加载。

    5.plot接口序列化为dot格式文件，并调用第三方工具dot画出计算图。


Optimizer类的设计思路：

    1.初始化时传入需要更新的参数。

    2.zero_grad接口进行梯度重置。

    3.step接口进行一次梯度更新。

    4.add_hook接口在参数更新前进行hook函数的操作。


### ops模块

- `nn/` —— 源代码目录
  - `operations/` —— 所有ops接口 
    - `__init__.py` —— 暴露接口
    - `activation_ops.py` —— 激活函数算子
    - `common_ops.py` —— Tensor操作算子
    - `math_ops.py` —— 数学计算类算子
    - `nn_ops.py` —— nn类算子
    - `utils.py` —— 工具函数
  - `__init__.py` —— 暴露接口
  - `functional.py` —— 所有functional接口
  - `primitive.py` —— 算子构建基本单元

Primitive类的设计思路：

    1.重载__call__方法，取出输入的Tensor类中承载的真实数据，调用forward进行正向计算，并封装成Tensor返回。

    2.Tensor.backward接口中使用链式法则调用单算子反向计算函数Primitive.backward完成自动微分。

# TODOList

1. 使用cupy支持GPU。
2. 使用pybind支持算子在CPU和cuda的实现。
3. 完善_type_check，支持可变输入的Tensor。
4. 完善dataset模块，支持Sample类。



# 展望

未来支持的特性包括：

## 元模块模版

    （基础模版）提供元模块模版，用户可以通过yaml定义组建模型，自动生成编译好的图，从而进行组合。
    （支持定制）对于自定义的模型， 可以通过最小粒度的元类型模版进行搭建，再调用编译接口，生成编译好的子图并保存。

## 动静统一

    合并动态图和静态图的概念，用户组件好的模型将自动生成编译成整图，达到最优性能执行。
