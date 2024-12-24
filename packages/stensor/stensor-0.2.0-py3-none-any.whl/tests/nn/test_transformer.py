import numpy as np
from stensor.model import Transformer
from stensor.config import Config, no_grad
from stensor.dataset import DataLoader, Dataset
from stensor.common import Tensor
from stensor.nn.opt.optimizer import SGD, ClipGrad, MomentumSGD, Adam
from stensor.nn import accuracy
from stensor.ops import functional as F


#=============================== step1 :prepare dataset ===============================
# S: Symbol that shows starting of decoding input
# E: Symbol that shows starting of decoding output
# P: Symbol that will fill in blank sequence if current batch data size is short than time steps
sentences = [
        # enc_input           dec_input         dec_output
        ['ich mochte ein bier P', 'S i want a beer .', 'i want a beer . E'],
        ['ich mochte ein cola P', 'S i want a coke .', 'i want a coke . E']
]

# Padding Should be Zero
src_vocab = {'P' : 0, 'ich' : 1, 'mochte' : 2, 'ein' : 3, 'bier' : 4, 'cola' : 5}
src_vocab_size = len(src_vocab)

tgt_vocab = {'P' : 0, 'i' : 1, 'want' : 2, 'a' : 3, 'beer' : 4, 'coke' : 5, 'S' : 6, 'E' : 7, '.' : 8}
tgt2word = {i: w for i, w in enumerate(tgt_vocab)}
src2word = {i: w for i, w in enumerate(src_vocab)}
tgt_vocab_size = len(tgt_vocab)

src_len = 5 # enc_input max sequence length
tgt_len = 6 # dec_input(=dec_output) max sequence length


def make_data(sentences):
    enc_inputs, dec_inputs, dec_outputs = [], [], []
    for i in range(len(sentences)):
      enc_input = [[src_vocab[n] for n in sentences[i][0].split()]] # [[1, 2, 3, 4, 0], [1, 2, 3, 5, 0]]
      dec_input = [[tgt_vocab[n] for n in sentences[i][1].split()]] # [[6, 1, 2, 3, 4, 8], [6, 1, 2, 3, 5, 8]]
      dec_output = [[tgt_vocab[n] for n in sentences[i][2].split()]] # [[1, 2, 3, 4, 8, 7], [1, 2, 3, 5, 8, 7]]

      enc_inputs.extend(enc_input)
      dec_inputs.extend(dec_input)
      dec_outputs.extend(dec_output)

    return Tensor(np.array(enc_inputs)), Tensor(np.array(dec_inputs)), Tensor(np.array(dec_outputs))

enc_inputs, dec_inputs, dec_outputs = make_data(sentences)
print(enc_inputs, dec_inputs, dec_outputs)
# enc_inputs=Tensor(np.array([[1, 2, 3, 4, 0],[1, 2, 3, 5, 0]]))
# dec_inputs=Tensor(np.array([[6, 1, 2, 3, 4, 8],[6, 1, 2, 3, 5, 8]]))
# dec_outputs=Tensor(np.array([[1, 2, 3, 4, 8, 7],[1, 2, 3, 5, 8, 7]]))


class MyDataSet(Dataset):
    def __init__(self,enc_inputs, dec_inputs, dec_outputs):
        super(MyDataSet,self).__init__()
        self.enc_inputs = enc_inputs
        self.dec_inputs = dec_inputs
        self.dec_outputs = dec_outputs
        
    def __len__(self):
        # 我们前面的enc_inputs.shape = [2,5],所以这个返回的是2
        return self.enc_inputs.shape[0] 
    
    # 根据idx返回的是一组 enc_input, dec_input, dec_output
    def __getitem__(self, idx):
        return self.enc_inputs, self.dec_inputs, self.dec_outputs

# 构建DataLoader
loader = DataLoader(dataset=MyDataSet(enc_inputs, dec_inputs, dec_outputs), batch_size=2, shuffle=True)

#=============================== step2 :construct model and set config ===============================
model = Transformer()
lr = 0.001

#model.to_float16()
def test_transformer_plot_and_summary():
    model.plot(enc_inputs, dec_inputs, file_dir='./tests/model_resource/graph/', file_name='transformer')
    print("================current_name_and_submodules====================")
    print(model.current_name_and_submodules())
    print("================current_submodules====================")
    print(model.current_submodules())
    print("================All names_and_submodules====================")
    print(len(list(model.names_and_submodules())))
    for n, m in model.names_and_submodules():
        print(n,m)
    print("================submodules====================")
    print(model.submodules())
    print("================All names_and_parameters====================")
    print(len(list(model.names_and_parameters())))
    for n, p in model.names_and_parameters():
        print(n, p.shape, p)
    print("================total parameters counts====================")
    print(model.total_parameters_count())

#=============================== step3 :model construction ===============================
if Config.gpu_enable:
    Config.device = "gpu"
    model.to_gpu()
elif Config.npu_enable:
    Config.device = "npu"
    model.to_npu()
else:
    Config.device = "cpu"

if Config.gpu_enable:
    enc_inputs, dec_inputs, dec_outputs = enc_inputs.to_gpu(), dec_inputs.to_gpu(), dec_outputs.to_gpu()
elif Config.npu_enable:
    enc_inputs, dec_inputs, dec_outputs = enc_inputs.to_npu(), dec_inputs.to_npu(), dec_outputs.to_npu()
    
def test_transformer_train():
    opt = MomentumSGD(model.parameters(), lr=lr)
    #opt.add_hook(ClipGrad(100))
    print("==============start train Transform===========")
    for i in range(100):
        for _ in loader:
            #enc_inputs, dec_inputs, dec_outputs = get_data()
            outputs= model(enc_inputs, dec_inputs)
            #print("enc_inputs: ", enc_inputs)
            #print("dec_inputs: ", dec_inputs)
            loss = F.softmax_cross_entropy(outputs, dec_outputs.view(-1), reduction='mean')
            #loss = F.softmax_cross_entropy(outputs, dec_outputs.view(-1))
            acc = accuracy(outputs, dec_outputs.view(-1))
            print("i:", i,", loss:", loss.item, ", acc:", acc)
            opt.zero_grad()
            loss.backward()
            opt.step()
            #print("================parameters====================")
            #for n, p in model.names_and_parameters():
                #print(n,p)
    #model.plot(enc_inputs, dec_inputs)
    print("==============end train Transform===========")

    model.save_weights('./tests/model_resource/Transformer_msgd_lr1e4_step100.npz')


# 原文使用的是大小为4的beam search，这里为简单起见使用更简单的greedy贪心策略生成预测，不考虑候选，每一步选择概率最大的作为输出
# 如果不使用greedy_decoder，那么我们之前实现的model只会进行一次预测得到['i']，并不会自回归，所以我们利用编写好的Encoder-Decoder来手动实现自回归（把上一次Decoder的输出作为下一次的输入，直到预测出终止符）
def greedy_decoder(model, enc_input, start_symbol):
    """enc_input: [1, seq_len] 对应一句话"""
    enc_outputs = model.encoder(enc_input) # enc_outputs: [1, seq_len, 512]
    # 生成一个1行0列的，和enc_inputs.data类型相同的空张量，待后续填充
    dec_input = Tensor(np.array([[]], dtype=int)) # .data避免影响梯度信息
    print("dec_input: ",dec_input.shape)
    print(Tensor(np.array([[0]])).shape)
    next_symbol = start_symbol
    flag = True
    while flag:
        # dec_input.detach() 创建 dec_input 的一个分离副本
        # 生成了一个 只含有next_symbol的（1,1）的张量
        # -1 表示在最后一个维度上进行拼接cat
        # 这行代码的作用是将next_symbol拼接到dec_input中，作为新一轮decoder的输入
        dec_input = F.concat((dec_input, Tensor(np.array([[next_symbol]], dtype=int))), axis=-1) # dec_input: [1,当前词数]
        print(dec_input,dec_input.shape,dec_input.dtype)
        dec_outputs = model.decoder(dec_input, enc_input, enc_outputs) # dec_outputs: [1, tgt_len, d_model]
        projected = model.projection(dec_outputs) # projected: [1, 当前生成的tgt_len, tgt_vocab_size]
        # max返回的是一个元组（最大值，最大值对应的索引），所以用[1]取到最大值对应的索引, 索引就是类别，即预测出的下一个词
        # keepdim为False会导致减少一维
        #print(projected.squeeze(0).max(axis=-1, keepdims=False))
        print(projected.shape)
        #prob = projected.squeeze(0).max(axis=-1, keepdims=False)
        prob = projected.squeeze(0).data
        prob = np.argmax(prob, axis=-1, keepdims=False)
        print(prob) # prob: [1],
        #raise ValueError
        # prob是一个一维的列表，包含目前为止依次生成的词的索引，最后一个是新生成的（即下一个词的类别）
        # 因为注意力是依照前面的词算出来的，所以后生成的不会改变之前生成的
        next_symbol = prob.data[-1]
        if next_symbol == tgt_vocab['.'] or next_symbol == tgt_vocab['E']:
            flag = False
        print(next_symbol)
    return dec_input  # dec_input: [1,tgt_len]

def greedy_decoder_gpu(model, enc_input, start_symbol):
    
    """enc_input: [1, seq_len] 对应一句话"""
    enc_outputs = model.encoder(enc_input) # enc_outputs: [1, seq_len, 512]
    # 生成一个1行0列的，和enc_inputs.data类型相同的空张量，待后续填充
    dec_input = Tensor(np.array([[]], dtype=int)).to_gpu() # .data避免影响梯度信息
    print("dec_input: ",dec_input.shape)
    next_symbol = start_symbol
    flag = True
    while flag:
        # dec_input.detach() 创建 dec_input 的一个分离副本
        # 生成了一个 只含有next_symbol的（1,1）的张量
        # -1 表示在最后一个维度上进行拼接cat
        # 这行代码的作用是将next_symbol拼接到dec_input中，作为新一轮decoder的输入
        dec_input = F.concat((dec_input, Tensor(np.array([[next_symbol]], dtype=int))).to_gpu(), axis=-1) # dec_input: [1,当前词数]
        print(dec_input,dec_input.shape,dec_input.dtype)
        dec_outputs = model.decoder(dec_input, enc_input, enc_outputs) # dec_outputs: [1, tgt_len, d_model]
        projected = model.projection(dec_outputs) # projected: [1, 当前生成的tgt_len, tgt_vocab_size]
        # max返回的是一个元组（最大值，最大值对应的索引），所以用[1]取到最大值对应的索引, 索引就是类别，即预测出的下一个词
        # keepdim为False会导致减少一维
        #print(projected.squeeze(0).max(axis=-1, keepdims=False))
        print(projected.shape)
        #prob = projected.squeeze(0).max(axis=-1, keepdims=False)
        prob = projected.squeeze(0)
        prob_max, prob = F.max(prob, axis=-1, keepdims=False)
        #prob = np.argmax(prob, axis=-1, keepdims=False)
        print(prob_max, prob) # prob: [1],
        
        
        #raise ValueError
        # prob是一个一维的列表，包含目前为止依次生成的词的索引，最后一个是新生成的（即下一个词的类别）
        # 因为注意力是依照前面的词算出来的，所以后生成的不会改变之前生成的
        next_symbol = prob[-1].data.item()
        print(next_symbol, type(next_symbol))
        if next_symbol == tgt_vocab['.'] or next_symbol == tgt_vocab['E']:
            flag = False
        print(next_symbol)
    return dec_input  # dec_input: [1,tgt_len]

def greedy_decoder_npu(model, enc_input, start_symbol):
    
    """enc_input: [1, seq_len] 对应一句话"""
    enc_outputs = model.encoder(enc_input) # enc_outputs: [1, seq_len, 512]
    # 生成一个1行0列的，和enc_inputs.data类型相同的空张量，待后续填充
    dec_input = Tensor(np.array([[]], dtype=int)).to_npu() # .data避免影响梯度信息
    print("dec_input: ",dec_input.shape)
    next_symbol = start_symbol
    flag = True
    while flag:
        # dec_input.detach() 创建 dec_input 的一个分离副本
        # 生成了一个 只含有next_symbol的（1,1）的张量
        # -1 表示在最后一个维度上进行拼接cat
        # 这行代码的作用是将next_symbol拼接到dec_input中，作为新一轮decoder的输入
        dec_input = F.concat((dec_input, Tensor(np.array([[next_symbol]], dtype=int))).to_npu(), axis=-1) # dec_input: [1,当前词数]
        print(dec_input,dec_input.shape,dec_input.dtype)
        dec_outputs = model.decoder(dec_input, enc_input, enc_outputs) # dec_outputs: [1, tgt_len, d_model]
        projected = model.projection(dec_outputs) # projected: [1, 当前生成的tgt_len, tgt_vocab_size]
        # max返回的是一个元组（最大值，最大值对应的索引），所以用[1]取到最大值对应的索引, 索引就是类别，即预测出的下一个词
        # keepdim为False会导致减少一维
        #print(projected.squeeze(0).max(axis=-1, keepdims=False))
        print(projected.shape)
        #prob = projected.squeeze(0).max(axis=-1, keepdims=False)
        prob = projected.squeeze(0)
        prob_max, prob = F.max(prob, axis=-1, keepdims=False)
        #prob = np.argmax(prob, axis=-1, keepdims=False)
        print(prob_max, prob) # prob: [1],
        
        
        #raise ValueError
        # prob是一个一维的列表，包含目前为止依次生成的词的索引，最后一个是新生成的（即下一个词的类别）
        # 因为注意力是依照前面的词算出来的，所以后生成的不会改变之前生成的
        next_symbol = prob[-1].data.item()
        print(next_symbol, type(next_symbol))
        if next_symbol == tgt_vocab['.'] or next_symbol == tgt_vocab['E']:
            flag = False
        print(next_symbol)
    return dec_input  # dec_input: [1,tgt_len]


def test_transformer_infer():
    # 测试
    model.load_weights('./tests/model_resource/Transformer_msgd_lr1e4_step100.npz')
    if Config.gpu_enable:
        model.to_gpu()
    elif Config.npu_enable:
        model.to_npu()
    #evalation
    with no_grad():
        # 手动从loader中取一个batch的数据
        for i in range(len(enc_inputs)):
            if Config.gpu_enable:
                greedy_dec_input = greedy_decoder_gpu(model, enc_inputs[i].view(1, -1), start_symbol=tgt_vocab['S'])
            elif Config.npu_enable:
                greedy_dec_input = greedy_decoder_npu(model, enc_inputs[i].view(1, -1), start_symbol=tgt_vocab['S'])
            else:
                greedy_dec_input = greedy_decoder(model, enc_inputs[i].view(1, -1), start_symbol=tgt_vocab['S'])
            print("===============",greedy_dec_input)
            predict  = model(enc_inputs[i].view(1, -1), greedy_dec_input) # predict: [batch_size * tgt_len, tgt_vocab_size]
            #predict = predict.data.max(dim=-1, keepdim=False)[1]
            print(predict.shape)
            predict = np.argmax(predict.data, axis=-1, keepdims=False)
            '''greedy_dec_input是基于贪婪策略生成的，而贪婪解码的输出是基于当前时间步生成的假设的输出。这意味着它可能不是最优的输出，因为它仅考虑了每个时间步的最有可能的单词，而没有考虑全局上下文。
            因此，为了获得更好的性能评估，通常会将整个输入序列和之前的假设输出序列传递给模型，以考虑全局上下文并允许模型更准确地生成输出
            '''
            print([src2word[n.item()] for n in enc_inputs[i].data], '->', [tgt2word[n.item()] for n in predict])
