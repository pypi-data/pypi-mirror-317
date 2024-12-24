import numpy as np
import math
from stensor.common import Tensor
from stensor.nn import accuracy
from stensor.ops import functional as F
from stensor.nn import layer as L
from stensor.nn.opt import optimizer
from stensor.dataset import Spiral, DataLoader
from stensor.config import no_grad


def get_spiral(train=True):
    seed = 1984 if train else 2020
    np.random.seed(seed=seed)

    num_data, num_class, input_dim = 100, 3, 2
    data_size = num_class * num_data
    x = np.zeros((data_size, input_dim), dtype=np.float32)
    t = np.zeros(data_size, dtype=np.int64)

    for j in range(num_class):
        for i in range(num_data):
            rate = i / num_data
            radius = 1.0 * rate
            theta = j * 4.0 + 4.0 * rate + np.random.randn() * 0.2
            ix = num_data * j + i
            x[ix] = np.array([radius * np.sin(theta),
                              radius * np.cos(theta)]).flatten()
            t[ix] = j
    # Shuffle
    indices = np.random.permutation(num_data * num_class)
    x = x[indices]
    t = t[indices]
    return x, t


def test_multi_classification_1():
    # toy dataset
    np.random.seed(0)
    x = Tensor(np.random.rand(3, 1))
    y = 5 + 2 * x

    x = Tensor(x)
    label = Tensor(np.array([0]))

    w = Tensor(np.zeros((1,2)))
    b = Tensor(np.zeros(2))

    def model(x):
        y = F.matmul(x, w) + b
        return y

    lr = 0.1
    iters = 1000
    for i in range(iters):
        y_pred = model(x)
        loss = F.softmax_cross_entropy(y_pred, label)

        w.cleargrad()
        b.cleargrad()
        loss.backward()
        
        w.data -= lr * w.grad.data
        b.data -= lr * b.grad.data
        if i % 100 == 0:
            print(w, b, loss.item)



def test_multi_classification_2():
    # toy dataset
    np.random.seed(0)
    x = np.random.rand(3, 3)

    x = Tensor(x)
    label = Tensor(np.array([0,1,2]))

    lr = 0.1
    iters = 1000

    model = L.TwoLinearNet(3, 10, 3)
    opt = optimizer.SGD(model.parameters(), lr)

    for i in range(iters):
        y_pred = model(x)
        loss = F.softmax_cross_entropy(y_pred, label)

        model.cleargrads()
        loss.backward()
        opt.step()
        if i % 100 == 0:
            print(i, loss.item)


def test_multi_classification_3():

    # 1. set hyper-parameter
    max_epoch = 5
    batch_size = 30
    hidden_size = 100
    lr = 0.1

    # 2. read dataset / construct model / create optimizer
    x, t = get_spiral(train=True)

    model = L.MLP(2, (4, 3), 3)
    opt = optimizer.SGD(model.parameters(), lr)

    data_size = len(x)
    max_iter = math.ceil(data_size / batch_size)

    for epoch in range(max_epoch):
        # 3. permute dataset
        index = np.random.permutation(data_size)
        sum_loss = 0

        for i in range(max_iter):
            # 4. batch size dataset
            batch_index = index[i * batch_size : (i + 1) * batch_size]
            batch_x, batch_t = x[batch_index], t[batch_index]


            #5.backward and get gradient / update parameter
            y = model(batch_x)
            loss = F.softmax_cross_entropy(y, batch_t)
            model.cleargrads()
            loss.backward()
            opt.step()
    

            sum_loss += float(loss.data) * len(batch_t)

        avg_loss = sum_loss / data_size
        print("epoch: ", epoch, ", loss: ", loss.item)


def test_multi_classification_4():

    # 1. set hyper-parameter
    max_epoch = 5
    batch_size = 30
    hidden_size = 10
    lr = 1.0

    # 2. read dataset / construct model / create optimizer
    train_set = Spiral(train=True)
    test_set = Spiral(train=False)
    train_loader = DataLoader(train_set, batch_size)
    test_loader = DataLoader(test_set, batch_size, shuffle=False)

    model = L.MLP(2, (hidden_size, hidden_size), 3)
    print(list(train_loader)[0][0].shape)
        
    #model.plot(Tensor(np.zeros((30, 2))))
    opt = optimizer.SGD(model.parameters(), lr)

    for epoch in range(max_epoch):
        sum_loss, sum_acc = 0, 0

        # 3. train
        for x, t in train_loader:
            y = model(x)
            loss = F.softmax_cross_entropy(y, t)
            acc = accuracy(y, t)
            model.cleargrads()
            loss.backward()
            opt.step()

            sum_loss += float(loss.data) * len(t)
            sum_acc += float(acc) * len(t)

        
        print('epoch: {}'.format(epoch + 1))
        print('train loss: {:.4f}, accuracy: {:.4f}'.format(
            sum_loss / len(train_set), sum_acc / len(train_set)))

        # 4. predict
        sum_loss, sum_acc = 0, 0
        with no_grad():
            for x, t in test_loader:
                y = model(x)
                loss = F.softmax_cross_entropy(y, t)
                acc = accuracy(y, t)
                model.cleargrads()

                sum_loss += float(loss.data) * len(t)
                sum_acc += float(acc) * len(t) 

        print('epoch: {}'.format(epoch + 1))
        print('test loss: {:.4f}, accuracy: {:.4f}'.format(
            sum_loss / len(test_set), sum_acc / len(test_set)))
