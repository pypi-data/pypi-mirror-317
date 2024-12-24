import os
import matplotlib.pyplot as plt

import stensor.nn as nn
from stensor.dataset import MNIST, DataLoader
from stensor.nn import SGD, Adam, accuracy
from stensor.ops import functional as F
from stensor.config import no_grad


def test_mnist():
    #1.set hyper-parameter
    max_epoch = 5
    batch_size = 100
    hidden_size = 100
    lr = 0.01

    #2.dataset
    train_set = MNIST(train=True)
    test_set = MNIST(train=False)
    train_loader = DataLoader(train_set, batch_size)
    test_loader = DataLoader(test_set, batch_size, shuffle=False)

    #example train dataset
    x, t = train_set[0]
    # plt.imshow(x.reshape(28, 28), cmap='gray')
    # plt.axis('off')
    # plt.show()
    # print('label:', t)

    #3.model, optimizer
    model = nn.MLP(784, (hidden_size, hidden_size), 10, activation=F.relu)
    opt = SGD(model.parameters())

    for epoch in range(max_epoch):
        sum_loss, sum_acc = 0, 0

        for x, t in train_loader:
            y = model(x)
            loss = F.softmax_cross_entropy(y, t)
            acc = accuracy(y, t)
            model.cleargrads()
            loss.backward()
            opt.step()

            sum_loss += float(loss.data) * len(t)
            sum_acc =+ float(acc) * len(t)
        
        print('epoch: {}'.format(epoch + 1))
        print('train loss: {:4f}, accuracy: {:.4f}'.format(
            sum_loss / len(train_set), sum_acc / batch_size
        ))

        sum_loss, sum_acc = 0, 0
        with no_grad():
            for x, t in test_loader:
                y = model(x)
                loss = F.softmax_cross_entropy(y, t)
                acc = accuracy(y, t)
                
                sum_loss += float(loss.data) * len(t)
                sum_acc =+ float(acc) * len(t)

        print('test loss: {:4f}, accuracy: {:.4f}'.format(
            sum_loss / len(test_set), sum_acc / batch_size
        ))


def test_mnist_save_and_load():
    #1.set hyper-parameter
    max_epoch = 5
    batch_size = 100
    hidden_size = 10
    lr = 0.01

    #2.dataset
    train_set = MNIST(train=True)
    train_loader = DataLoader(train_set, batch_size)

    model = nn.MLP(784, (hidden_size, hidden_size), 10, activation=F.relu)
    opt = SGD(model.parameters())

    if os.path.exists('./mnist_mlp.npz'):
        print("===========load mnist mlp model===============")
        model.load_weights('./mnist_mlp.npz')

    for epoch in range(max_epoch):
        sum_loss = 0

        for x, t in train_loader:
            y = model(x)
            loss = F.softmax_cross_entropy(y, t)
            model.cleargrads()
            loss.backward()
            opt.step()
            sum_loss += float(loss.data) * len(t)
        
        print('epoch: {}, loss: {:.4f}'.format(
            epoch + 1, sum_loss / len(train_set)
        ))
    
    model.save_weights('./mnist_mlp.npz')
