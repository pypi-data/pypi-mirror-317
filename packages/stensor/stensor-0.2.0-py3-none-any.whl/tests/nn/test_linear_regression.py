import numpy as np

from stensor.common import Tensor
from stensor.ops import functional as F

# toy dataset
np.random.seed(0)
x = Tensor(np.random.rand(100, 1))
y = 5 + 2 * x

w = Tensor(np.zeros((1,1)))
b = Tensor(np.zeros(1))

def predict(x):
    # y = F.matmul(x, w) + F.broadcast_to(b, (100,1)) 
    y = F.matmul(x, w) + b
    print(x.shape, w.shape, b.shape ,y.shape)
    return y

def mean_squared_error(x0, x1):
    diff = x0 - x1
    return F.sum(diff ** 2) / len(diff)


def test_linear_regression():
    lr = 0.1
    iters = 10
    for i in range(iters):
        y_pred = predict(x)
        loss = mean_squared_error(y, y_pred)
        print(loss.item)
        w.cleargrad()
        b.cleargrad()
        loss.backward()
        
        w.data -= lr * w.grad.data
        b.data -= lr * b.grad.data
        print(w, b, loss.item)

test_linear_regression()