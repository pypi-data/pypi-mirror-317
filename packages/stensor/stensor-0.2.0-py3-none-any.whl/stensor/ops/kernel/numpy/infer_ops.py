import numpy as np

from .numpy_kernel import NumpyKernel


class TopK(NumpyKernel):
    def forward(self, x, k):

        # 使用 argpartition 找到前 k 个最大的元素的未排序索引
        partition_indices = np.argpartition(x, -k)[-k:]

        # 对这 k 个元素进行排序，以获得从大到小的顺序
        sorted_topk_indices = partition_indices[np.argsort(x[partition_indices])[::-1]]

        # 获取对应的 top k 值
        topk_values = x[sorted_topk_indices]

        return topk_values, sorted_topk_indices


    def backward(self, gy):
        raise NotImplementedError

class Multinomial(NumpyKernel):
    def forward(self, input_probs, num_samples):
        if np.any(input_probs < 0):
            # 如果存在负值，可以通过将所有值平移为非负来处理
            # 例如，添加一个常数使所有值变为非负
            min_value = input_probs.min()
            input_probs = input_probs - min_value + 1e-6  # 添加一个小常数以避免全为零

        # 归一化权重为概率
        probabilities = input_probs / np.sum(input_probs)

        # 使用 np.random.choice 进行抽样
        # replace=False 表示不放回抽样，类似于 torch.multinomial 的默认行为
        sampled_indices = np.random.choice(
            a=np.arange(len(input_probs)),
            size=num_samples,
            replace=False,
            p=probabilities
        )
        return sampled_indices

    def backward(self, gy):
        raise NotImplementedError
