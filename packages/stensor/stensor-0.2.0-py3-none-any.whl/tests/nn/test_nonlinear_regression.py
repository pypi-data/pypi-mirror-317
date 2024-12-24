import numpy as np
from stensor.common import Tensor
from stensor.ops import functional as F
from stensor.nn import layer as L
from stensor.nn.module import Module
from stensor.nn.opt import optimizer

# toy dataset
np.random.seed(0)
x = np.random.rand(10, 1)
y = np.sin(2 * np.pi * x) + np.random.rand(10, 1)

x = Tensor(x)
y = Tensor(y)

def test_nonlinear_regression_1():
    w1 = Tensor(np.random.rand(10, 1))
    b1 = Tensor(np.zeros(10))
    w2 = Tensor(np.random.rand(1, 10))
    b2 = Tensor(np.zeros(1))

    def predict(x):
        y = F.linear(x, w1, b1)
        y = F.sigmoid(y)
        y = F.linear(y, w2, b2)
        return y

    lr = 0.1
    iters = 1000
    for i in range(iters):
        y_pred = predict(x)
        loss = F.mean_squared_error(y, y_pred)

        w1.cleargrad()
        b1.cleargrad()
        w2.cleargrad()
        b2.cleargrad()

        loss.backward()
        
        w1.data -= lr * w1.grad.data
        b1.data -= lr * b1.grad.data
        w2.data -= lr * w2.grad.data
        b2.data -= lr * b2.grad.data
        if i == 999:
            print(w1, b1, w2, b2, loss)
            print(x)
            print(predict(x)- y)


def test_nonlinear_regression_2():
    l1 = L.Linear(1, 10)
    l2 = L.Linear(10, 1)

    def predict(x):
        y = l1(x)
        y = F.sigmoid(y)
        y = l2(y)
        return y
    
    lr = 0.2
    iters = 1000
    for i in range(iters):
        y_pred = predict(x)
        loss = F.mean_squared_error(y, y_pred)
        l1.cleargrads()
        l2.cleargrads()
        loss.backward()

        for l in [l1, l2]:
            for p in l.parameters():
                p.data -= lr * p.grad.data
        
        if i % 100 == 0:
            print(loss)


def test_nonlinear_regression_3():
    model = Module()
    model.l1 = L.Linear(1, 10)
    model.l2 = L.Linear(10, 1)

    def predict(model, x):
        y = model.l1(x)
        y = F.sigmoid(y)
        y = model.l2(y)
        return y
    
    lr = 0.2
    iters = 1000
    for i in range(iters):
        y_pred = predict(model, x)
        loss = F.mean_squared_error(y, y_pred)

        model.cleargrads()
        loss.backward()

        for p in model.parameters():
            p.data -= lr * p.grad.data
                
        if i % 100 == 0:
            print(loss)

def test_nonlinear_regression_4():
    model = L.TwoLinearNet(1, 10, 1)
    def predict(model, x):
        y = model.l1(x)
        y = F.sigmoid(y)
        y = model.l2(y)
        return y
    
    lr = 0.2
    iters = 1000
    for i in range(iters):
        y_pred = predict(model, x)
        loss = F.mean_squared_error(y, y_pred)

        model.cleargrads()
        loss.backward()

        for p in model.parameters():
            p.data -= lr * p.grad.data
                
        if i % 100 == 0:
            print(loss)


def test_nonlinear_regression_5():
    model = L.MLP(1, (20, 10), 1)
    def predict(model, x):
        y = model(x)
        return y
    
    lr = 0.2
    iters = 1000
    for i in range(iters):
        y_pred = predict(model, x)
        loss = F.mean_squared_error(y, y_pred)

        model.cleargrads()
        loss.backward()

        for p in model.parameters():
            p.data -= lr * p.grad.data
                
        if i % 100 == 0:
            print(loss)


def test_nonlinear_regression_6():
    
    np.random.seed(0)
    lr = 0.05
    iters = 1000
    hidden_size = 20

    model = L.MLP(1, (20, 10), 1)
    opt = optimizer.MomentumSGD(model.parameters(), lr, momentum=0.99)

    for i in range(iters):
        y_pred = model(x)
        loss = F.mean_squared_error(y, y_pred)

        model.cleargrads()
        loss.backward()
        opt.step()
                
        if i % 100 == 0:
            print(loss)

