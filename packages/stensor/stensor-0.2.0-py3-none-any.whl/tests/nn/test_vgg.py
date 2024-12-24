import numpy as np
from stensor.model import VGG16
from stensor.nn.opt.optimizer import SGD, ClipGrad
import stensor.ops.functional as F 

def test_vgg():
    max_epoch = 10
    batch_size = 30
    lr = 0.01

    # 2. read dataset / construct model / create optimizer
    
    model = VGG16(pretrained=False)
    #opt = SGD(lr).setup(model)
    opt = SGD(model.parameters(), lr=lr)
    opt.add_hook(ClipGrad(100))
    x = np.random.randn(1, 3, 224, 224).astype(np.float32)
    t = np.zeros((1, 1000)).astype(np.float32)
    t[0][0] =1

    model.plot(x, file_dir='./tests/model_resource/graph/', file_name='vgg')
    #model(x)
    for epoch in range(max_epoch):
        # 3. permute dataset

        #5.backward and get gradient / update parameter
        y = model(x)
        loss = F.mean_squared_error(y, t)
        model.cleargrads()
        loss.backward()
        opt.step()

        print("epoch:",(epoch + 1), ", loss:", loss.item)
