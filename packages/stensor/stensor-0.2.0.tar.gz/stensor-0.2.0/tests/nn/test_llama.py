import numpy as np

from stensor import Tensor, nn, Config
from stensor.ops import functional as F
import stensor.nn.opt as optim
from stensor.model import Llama, LlamaConfig


def test_llama():
    model = Llama(LlamaConfig())
    print("total_parameters_count: ",model.total_parameters_count())
    print("==============")
    for n, p in model.names_and_parameters():
        print(n, p.shape)
    print("==============")
    tokens = Tensor(np.array([[0,0],[1,1]]))

    model.train()
    # 损失函数,忽略为0的类别不对其计算loss（因为是padding无意义）
    criterion = nn.SoftmaxCrossEntropy()

    optimizer = optim.MomentumSGD(model.parameters(), lr=0.01)
    #optimizer.add_hook(optim.ClipGrad(10))
    # 训练开始
    for epoch in range(10):
        #tokes = Tensor(np.random.rand(2, 2))
        outputs = model(tokens) # outputs: [batch_size * tgt_len, tgt_vocab_size]
        # outputs: [batch_size * tgt_len, tgt_vocab_size], dec_outputs: [batch_size, tgt_len]
        loss = criterion(outputs, Tensor(np.array([1, 1, 0, 0])))  # 将dec_outputs展平成一维张量

        # 更新权重
        optimizer.zero_grad()
        #torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        loss.backward()
        optimizer.step()

        print(f'Epoch [{epoch + 1}/10], Loss: {loss.item}')