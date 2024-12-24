import time
import numpy as np
import pytest
import pandas as pd

from stensor.model import GPTConfig, GPTModel, PretrainDatasetFromBin, PretrainDataset, SFTDataset
from stensor import Tensor, MomentumSGD, Config, ClipGrad, no_grad
from stensor.dataset import  DataLoader
from stensor.ops import functional as F

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(r'./tests/model_resource/gpt_tokenizer')

def test_gpt_model_init():
    config = GPTConfig(batch_size=2, cross_entropy_reduction='sum')
    model = GPTModel(config)
    print("total_parameters_count: ",model.total_parameters_count())
    print("==============")
    for n, p in model.names_and_parameters():
        print(n, p.shape)
    print("==============")
    tokens = Tensor(np.array([[0,0],[1,1]]))
    label = Tensor(np.array([1, 1, 2, 2]))
    model.train()
    optimizer = MomentumSGD(model.parameters(), lr=0.01)
    optimizer.add_hook(ClipGrad(10))

    for epoch in range(10):
        _, loss = model(tokens, label) 
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f'Epoch [{epoch + 1}/10], Loss: {loss.item}')

    model.plot(tokens, label, outputs=loss, file_dir='./tests/model_resource/graph/', file_name='gpt')
    logits, idx_next = model.eval_one(tokens)
    print("logitics", logits)
    print("logitics after argmax: ", idx_next)
    assert idx_next == label


@pytest.mark.skip(reason="unspoort pretrain dataset from bin!")
def test_gpt_model_pretrain_dataset_from_bin():
    config = GPTConfig(batch_size=1, cross_entropy_reduction='sum')
    data_path_list = [r"D:\download\pretrain_data.bin"]
    train_ds = PretrainDatasetFromBin(data_path_list, max_length=config.max_seq_len, memmap=True)
    train_loader = DataLoader(train_ds, batch_size=config.batch_size, shuffle=True)

    device = "gpu" if Config.gpu_enable else "cpu"
    model = GPTModel(config).to(device)
    model.train()
    optimizer = MomentumSGD(model.parameters(), lr=0.001)
    print("total_parameters_count: ",model.total_parameters_count())
    print("==============")
    for n, p in model.names_and_parameters():
        print(n, p.shape, p.dtype, p.device)
    print("==============")
    
    X, Y = next(iter(train_loader))
    X, Y = Tensor(X), Tensor(Y)
    _, loss = model(X, Y)
    model.plot(X, Y, outputs=loss, file_dir='gpt_graph')
    
    for step, (X, Y) in enumerate(train_loader):
        time0 = time.time()
        X, Y = Tensor(X).to(device), Tensor(Y).to(device)
        time1 = time.time()
        _, loss = model(X, Y)
        #model.plot(X, Y, outputs=loss)
        time2 = time.time()
        optimizer.zero_grad()
        time3 = time.time()
        loss.backward()
        time4 =time.time()
        optimizer.step()
        time5 = time.time()
        print(f"step [{step}], Loss: {loss.item}, data cost :{time1-time0}, foward cost: {time2-time1}, "\
              f"zero_grad cost: {time3-time2},  backward cost: {time4-time3}, optimizer step cost: {time5-time4}")
        if step == 20:
            break


@pytest.mark.skip(reason="unspoort pretrain dataset from bin!")
def test_gpt_model_pretrain_dataset_from_bin_accumulation_steps():
    config = GPTConfig(batch_size=1)
    data_path_list = [r"D:\download\pretrain_data.bin"]
    train_ds = PretrainDatasetFromBin(data_path_list, max_length=config.max_seq_len, memmap=True)
    train_loader = DataLoader(train_ds, batch_size=config.batch_size, shuffle=True)

    device = "gpu" if Config.gpu_enable else "cpu"
    model = GPTModel(config).to(device)
    model.train()
    optimizer = MomentumSGD(model.parameters(), lr=0.01)
    print("total_parameters_count: ",model.total_parameters_count())
    print("==============")
    for n, p in model.names_and_parameters():
        print(n, p.shape, p.dtype, p.device)
    print("==============")
    
    accumulation_steps = 8
    start_time = time.time()
    for step, (X, Y) in enumerate(train_loader):
        X, Y = Tensor(X).to(device), Tensor(Y).to(device)
        _, loss = model(X, Y)
        loss.backward()
        # 每 accumulation_steps 次更新一次权重
        if (step + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()

        if step % 10 == 0:
            print(f"step {step}, loss: {loss.item:.6f}, lr: {optimizer.lr:.6f}, cost time: {time.time() - start_time:.6f}")

        if step ==20:
            break
    # 处理剩余的梯度，如果数据集大小不能整除 accumulation_steps
    if (step + 1) % accumulation_steps != 0:
        optimizer.step()
        optimizer.zero_grad()
        model.save_weights('./gpt_model.npz')


def test_gpt_model_forward_backward_accuary():

    config = GPTConfig(batch_size=1, num_layers=1)

    df = pd.read_csv(r"./tests/model_resource/pretrain_data_100.csv")
    #df = df.sample(frac=1.0)
    train_ds = PretrainDataset(df, tokenizer, max_length=config.max_seq_len)
    train_loader = DataLoader(train_ds, batch_size=config.batch_size, shuffle=False)
    print("dataset length: ", len(train_ds))
    device = "gpu" if Config.gpu_enable else "cpu"
    #Config.debug=True
    model = GPTModel(config)
    from stensor.nn import register_print_hooks
    register_print_hooks(model)
    
    model.load_weights(r'..\..\note\性能优化\step4精度对比\pretrain_512_data_100.npz')
    model.to_float32().to(device)
    model.train()
    
    print("total_parameters_count: ",model.total_parameters_count())
    print("==============")
    for n, p in model.names_and_parameters():
        print(n, p.shape, p.dtype, p.device)
    print("==============")
    for n, m in model.names_and_submodules():
        print(n, m)

    for step, (X, Y, loss_mask) in enumerate(train_loader):
        print("X:", tokenizer.decode(X.tolist()[0]))
        print("Y:", tokenizer.decode(Y.tolist()[0]))
        #X, Y, loss_mask = Tensor(X).to(device), Tensor(Y).to(device), Tensor(loss_mask).to(device)
        X, Y, loss_mask = Tensor(X).to(device), Tensor(Y).to(device), Tensor(loss_mask).to(device)
        break
    

    #X, Y, loss_mask = Tensor(X).to(device), Tensor(Y).to(device), Tensor(loss_mask).to(device)
    _, loss = model(X, Y, loss_mask=loss_mask)
    assert np.isclose(loss.data, 7.73052, rtol=1e-3)
    
    loss.backward()
    tmp_save = {}
    for n, p in model.names_and_parameters():
        if p.grad is not None:
            print(n, "_grad:", p.grad.dtype, p.grad.norm().item, p.grad.mean().item,p.grad.max()[0].item,p.grad.min()[0].item)
            assert f"{p.grad.dtype}" == "float32"
            if device == "gpu":
                tmp_save.update({n: (p.grad.norm().item.get(), p.grad.mean().item.get(), \
                    p.grad.max()[0].item.get(), p.grad.min()[0].item.get())})
            else:
                tmp_save.update({n: (p.grad.norm().item, p.grad.mean().item, p.grad.max()[0].item, p.grad.min()[0].item)})

    assert np.isclose(tmp_save["tok_embeddings.embedding"], (3.5437827, -2.781265e-06, 0.18048781, -0.16779736), rtol=4e-4).all()
    assert np.isclose(tmp_save["layers.0.attention.wq.W"], ((0.22352134, 2.5657556e-07, 0.0027212496, -0.0027290958)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.attention.wk.W"], ((0.24987221, -2.654685e-06, 0.0051101586, -0.0050805053)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.attention.wv.W"], ((3.1293757, -3.9006016e-05, 0.07678984, -0.062073566)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.attention.wo.W"], ((6.755783, 6.2493265e-05, 0.119118266, -0.105179094)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.attention_norm.gamma"], ((0.06373619, 0.00013757597, 0.011773646, -0.009735157)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.ffn_norm.gamma"], ((0.19595677, -0.008162505, 0.0016817009, -0.01850988)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.feed_forward.w1.W"], ((2.0459507, -2.5858031e-05, 0.021885987, -0.024602845)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.feed_forward.w2.W"], ((2.008518, -1.208174e-07, 0.027723785, -0.02803021)), rtol=1e-4).all()
    assert np.isclose(tmp_save["layers.0.feed_forward.w3.W"], ((6.4428797, -2.7884591e-06, 0.09831646, -0.08265146)), rtol=1e-4).all()
    assert np.isclose(tmp_save["norm.gamma"], ((0.1047382, 0.0036617336, 0.012038686, -0.008144658)), rtol=1e-4).all()


def test_gpt_model_pretrain_dataset_accumulation_steps():
    import pandas as pd
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(r'./tests/model_resource/gpt_tokenizer')
    
    config = GPTConfig(batch_size=1, num_layers=8)
    #config = GPTConfig(batch_size=1, hidden_size=8, num_layers=1, max_seq_len=4)
    df = pd.read_csv(r"./tests/model_resource/pretrain_data_100.csv")
    #df = df.sample(frac=1.0)
    train_ds = PretrainDataset(df, tokenizer, max_length=config.max_seq_len)
    train_loader = DataLoader(train_ds, batch_size=config.batch_size, shuffle=False)
    print("dataset length: ", len(train_ds))
    device = "gpu" if Config.gpu_enable else "cpu"
    model = GPTModel(config)
    # from stensor.nn import register_print_hooks
    # register_print_hooks(model)
    #model.load_weights(r"./tests/model_resource/small_model.npz")
    model.to(device)
    
    model.train()
    
    optimizer = MomentumSGD(model.parameters(), lr=0.01)
    print("total_parameters_count: ",model.total_parameters_count())
    print("==============")
    for n, p in model.names_and_parameters():
        print(n, p.shape, p.dtype, p.device)
    print("==============")
    for n, m in model.names_and_submodules():
        print(n, m)
    accumulation_steps = 1
    epochs = 1
    # for step, (X, Y, loss_mask) in enumerate(train_loader):
    #     print("X:", tokenizer.decode(X.tolist()[0]))
    #     print("Y:", tokenizer.decode(Y.tolist()[0]))
    #     X, Y, loss_mask = Tensor(X).to(device), Tensor(Y).to(device), Tensor(loss_mask).to(device)
    #     break
    
    start_time = time.time()
    for epoch in range(epochs):
        for step, (X, Y, loss_mask) in enumerate(train_loader):
            X, Y, loss_mask = Tensor(X).to(device), Tensor(Y).to(device), Tensor(loss_mask).to(device)
            _, loss = model(X, Y, loss_mask=loss_mask)
            loss.backward()
            # for n, p in model.names_and_parameters():
            #     if p.grad is not None:          
            #         print(n, "grad",p.grad.dtype, p.grad.shape, p.grad)       
            
            # 每 accumulation_steps 次更新一次权重
            if (step + 1) % accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()

            if (step + 1) % 10 == 0:
                print(f"epoch {epoch}, step {step}, loss: {loss.item:.6f}, lr: {optimizer.lr:.6f}, "\
                      f"cost time: {time.time() - start_time:.6f}")
                #model.save_weights(f'./test_gpt_model_pretrain_dataset_step_{(step+1)}.npz')
                
        # # 处理剩余的梯度，如果数据集大小不能整除 accumulation_steps
        if (step + 1) % accumulation_steps != 0:
            optimizer.step()
            optimizer.zero_grad()
    model.save_weights('./tests/model_resource/test_gpt_model_pretrain_dataset_0.npz')


def test_gpt_model_pretrain_eval_one_token():
    device = "gpu" if Config.gpu_enable else "cpu"
    config = GPTConfig(batch_size=1, num_layers=1)
    model = GPTModel(config)
    
    model.load_weights(r"./tests/model_resource/test_gpt_model_pretrain_dataset_0.npz")
    model = model.eval().to(device)
    
    prompt = '我们生产的食品消泡剂，具有可以快速消除泡沫的'
    prompt = tokenizer.bos_token + prompt
    x = tokenizer(prompt).data['input_ids']
    print("prompt after tokenizer: ", x)
    print("prompt after tokenizer decode: ", tokenizer.decode(x))
    x = Tensor(np.array(x), requires_grad=False).to(device)
    x = x[None, ...]

    logits, idx_next = model.eval_one(x)
    print("logitics after argmax: ", idx_next)
    answer = tokenizer.decode(idx_next.data.tolist())
    print("answer decode: ", answer)


#@pytest.mark.skip(reason="eval after pretrain")
def test_gpt_model_pretrain_eval():
    device = "gpu" if Config.gpu_enable else "cpu"
    config = GPTConfig(batch_size=1, num_layers=8)
    model = GPTModel(config)
    model.load_weights(r"./tests/model_resource/test_gpt_model_pretrain_dataset_0.npz")
    model = model.eval().to(device)
    
    prompt_datas = [
        '我们生产的食品消泡剂，具有可以快速消除泡沫的',
        '程总在座谈中首先向学校的客人介绍了三一集团',
        '白癜风病人调节心理要偶尔也要屈服。能屈能伸',
        '对全校教学保障、教学建设、教学管理、教学运行和教学改革等',
        '有趣的是，库里在第三节上篮时被防守球员',
        '担任地点省市的区域运营中心的',
        '在党建展览馆，全体党员跟随解说员通过开天',
        '其中，热转印是将人像、风景等任意图像使用热转印墨水',
    ]

    # prompt_datas = [
    #     '椭圆和圆的区别',
    #     '中国关于马克思主义基本原理',
    #     '人类大脑的主要功能是',
    #     '万有引力是',
    #     '世界上人口最多的国家是',
    #     'DNA的全称是',
    #     '数学中π的值大约是',
    #     '世界上最高的山峰是',
    #     '太阳系中最大的行星是',
    #     '二氧化碳的化学分子式是',
    #     '地球上最大的动物是',
    #     '地球自转一圈大约需要',
    #     '杭州市的美食有',
    #     '江苏省的最好的大学',
    # ]
    messages_origin = []
    messages = messages_origin
    
    max_seq_len = config.max_seq_len
    temperature = 1
    top_k = 1
    rp = 1
    #rp = 1.05
    stream = True
    kv_cache = True
    
    qa_index = 0
    while True:
        if qa_index >= len(prompt_datas):
            break
        prompt = prompt_datas[qa_index]
        print('问题：', prompt)
        qa_index += 1

        prompt = tokenizer.bos_token + prompt
        start = time.time()
        
        messages = []
        messages.append({"role": "user", "content": prompt})

        # print(messages)
        new_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )[-(max_seq_len - 1):]

        x = tokenizer(prompt).data['input_ids']
        x = Tensor(np.array(x), requires_grad=False).to(device)
        x = x[None, ...]

        answer = new_prompt

        with no_grad():
            res_y = model.generate(x, tokenizer.eos_token_id, max_new_tokens=max_seq_len, temperature=temperature,
                                   top_k=top_k, rp=rp, stream=stream, kv_cache=kv_cache)
            print('回答：', end='')
            try:
                y = next(res_y)
            except StopIteration:
                print("No answer")
                continue

            history_idx = 0
            while y != None:
                answer = tokenizer.decode(y.data.reshape(-1,).tolist())
                if answer and answer[-1] == '�':
                    try:
                        y = next(res_y)
                    except Exception as e:
                        print("Error decoding answer: ", e)
                        break
                    continue
                # print(answer)
                if not len(answer):
                    try:
                        y = next(res_y)
                    except Exception as e:
                        print("Error not len(answer): ", e)
                        break
                    continue

                print(answer[history_idx:], end='', flush=True)
                
                try:
                    y = next(res_y)
                except Exception as e:
                    break
                history_idx = len(answer)
                if not stream:
                    break

            print('\n')

        end = time.time()
        print(end - start,'s')

@pytest.mark.skip(reason="sft after pretrain")
def test_gpt_model_single_sft_dataset_accumulation_steps():
    config = GPTConfig(batch_size=20, num_layers=1)
    #config = GPTConfig(batch_size=1, hidden_size=8, num_layers=1, max_seq_len=4)
    df = pd.read_csv(r"./tests/model_resource/sft_data_100.csv")
    #df = df.sample(frac=1.0)
    train_ds = SFTDataset(df, tokenizer, max_length=config.max_seq_len)
    train_loader = DataLoader(train_ds, batch_size=config.batch_size, shuffle=False)
    print("dataset length: ", len(train_ds))
    device = "gpu" if Config.gpu_enable else "cpu"
    model = GPTModel(config)
    #model.load_weights(r"./tests/model_resource/small_model.npz")
    model.to(device)
    
    model.train()
    
    optimizer = MomentumSGD(model.parameters(), lr=0.01)
    print("total_parameters_count: ",model.total_parameters_count())
    print("==============")
    for n, p in model.names_and_parameters():
        print(n, p.shape, p.dtype, p.device)
    print("==============")
    for n, m in model.names_and_submodules():
        print(n, m)
    accumulation_steps = 1
    epochs = 1
    # for step, (X, Y, loss_mask) in enumerate(train_loader):
    #     print("X:", tokenizer.decode(X.tolist()[0]))
    #     print("Y:", tokenizer.decode(Y.tolist()[0]))
    #     X, Y, loss_mask = Tensor(X).to(device), Tensor(Y).to(device), Tensor(loss_mask).to(device)
    #     break
    
    start_time = time.time()
    for epoch in range(epochs):
        for step, (X, Y, loss_mask) in enumerate(train_loader):
            X, Y, loss_mask = Tensor(X).to(device), Tensor(Y).to(device), Tensor(loss_mask).to(device)
            _, loss = model(X, Y, loss_mask=loss_mask)
            loss.backward()
            # for n, p in model.names_and_parameters():
            #     if p.grad is not None:          
            #         print(n, "grad",p.grad.dtype, p.grad.shape, p.grad)       
            
            # 每 accumulation_steps 次更新一次权重
            if (step + 1) % accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()

            if (step + 1) % 10 == 0:
                print(f"epoch {epoch}, step {step}, loss: {loss.item:.6f}, lr: {optimizer.lr:.6f}, "\
                      f"cost time: {time.time() - start_time:.6f}")
                #model.save_weights(f'./test_gpt_model_pretrain_dataset_step_{(step+1)}.npz')
                
        # # 处理剩余的梯度，如果数据集大小不能整除 accumulation_steps
        if (step + 1) % accumulation_steps != 0:
            optimizer.step()
            optimizer.zero_grad()
    model.save_weights('./tests/test_gpt_model_pretrain_dataset_0.npz')
