import numpy as np
from stensor.ops.operations.kernel.numpy.numpy_kernel import NumpyKernel
from stensor import Config
from stensor.ops.operations.kernel.numpy._impl import sum_to, pair, logsumexp, softmax, get_deconv_outsize, im2col_array, col2im_array


class Linear(NumpyKernel):
    def forward(self, x, W, b):
        y = np.matmul(x, W)
        if b is not None:
            y += b
        return y

    def backward(self, gy):
        x, W, b = self.xs[0], self.xs[1], self.xs[2]
        gb = None if b is None else sum_to(gy, b.shape)
        #only consider the dim of x or W less than 5.
        gx = np.matmul(gy, np.swapaxes(W, -1, -2))
        if gx.shape != x.shape:
            gx = sum_to(gx, x.shape)

        gW = np.matmul(np.swapaxes(x, -1, -2), gy)
        if gW.shape != W.shape:
            gW = sum_to(gW, W.shape)
        return gx, gW, gb


class BatchNorm(NumpyKernel):
    def __init__(self, mean, var, decay, eps):
        self.avg_mean = mean
        self.avg_var = var
        self.decay = decay
        self.eps = eps
        self.inv_std = None

    def forward(self, x, gamma, beta):
        assert x.ndim == 2 or x.ndim == 4

        x_ndim = x.ndim
        if x_ndim == 4:
            N, C, H, W = x.shape
            # (N, C, H, W) -> (N*H*W, C)
            x = x.transpose(0, 2, 3, 1).reshape(-1, C)

        #xp = cuda.get_array_module(x)

        if Config.train:
            mean = x.mean(axis=0)
            var = x.var(axis=0)
            inv_std = 1 / np.sqrt(var + self.eps)
            xc = (x - mean) * inv_std

            m = x.size // gamma.size
            s = m - 1. if m - 1. > 1. else 1.
            adjust = m / s  # unbiased estimation
            self.avg_mean *= self.decay
            self.avg_mean += (1 - self.decay) * mean
            self.avg_var *= self.decay
            self.avg_var += (1 - self.decay) * adjust * var
            self.inv_std = inv_std
        else:
            inv_std = 1 / np.sqrt(self.avg_var + self.eps)
            xc = (x - self.avg_mean) * inv_std
        y = gamma * xc + beta

        if x_ndim == 4:
            # (N*H*W, C) -> (N, C, H, W)
            y = y.reshape(N, H, W, C).transpose(0, 3, 1, 2)
        return y

    def backward(self, gy):
        gy_ndim = gy.ndim
        if gy_ndim == 4:
            N, C, H, W = gy.shape
            gy = gy.transpose(0, 2, 3, 1).reshape(-1, C)

        x, gamma, beta = self.inputs
        batch_size = len(gy)

        if x.ndim == 4:
            N, C, H, W = x.shape
            x = x.transpose(0, 2, 3, 1).reshape(-1, C)
        mean = x.sum(axis=0) / batch_size
        xc = (x - mean) * self.inv_std

        gbeta = gy.sum(axis=0)
        ggamma = (xc * gy).sum( axis=0)
        gx = gy - gbeta / batch_size - xc * ggamma / batch_size
        gx *= gamma * self.inv_std

        if gy_ndim == 4:
            gx = gx.reshape(N, H, W, C).transpose(0, 3, 1, 2)
        return gx, ggamma, gbeta


class LayerNorm(NumpyKernel):
    def __init__(self, eps=1e-5):
        self.eps = eps

    def forward(self, x, gamma, beta):
        self.x, self.gamma, self.beta = x, gamma, beta
        # 计算均值和方差
        self.mean = np.mean(x, axis=-1, keepdims=True)
        self.variance = np.var(x, axis=-1, keepdims=True)
        self.xmu = (x - self.mean)
        self.xivar = np.sqrt(self.variance + self.eps)
        # 归一化
        x_normalized = self.xmu / self.xivar
        
        # 缩放和平移
        output = gamma * x_normalized + beta
        return output


    def backward(self, gy):
        x = self.x
        xmu = self.xmu
        xivar = self.xivar
        gamma = self.gamma
        dout = gy

        N, _, D= x.shape
        
        dgamma = (dout*xmu/xivar).sum(axis=0,keepdims=False)
        dbeta = dout.sum(axis=0,keepdims=False)

        dlxhat = dout*gamma
        dxhatx = 1/xivar
        dlvar = -0.5*((gamma*xmu*xivar**(-3)*dout).sum(axis=-1,keepdims=True))
        dlvarx = 2*xmu/D
        dlmu = -1.*((dlxhat/xivar).sum(axis=-1,keepdims=True))-2.*((dlvar*xmu).sum(axis=-1,keepdims=True)/D)


        dx = dlxhat*dxhatx + dlvar*dlvarx + dlmu/D
        return dx, dgamma, dbeta


class RMSNorm(NumpyKernel):
    def __init__(self, eps=1e-5):
        self.eps = eps

    def forward(self, x, gamma):
        self.x, self.gamma = x, gamma
        self.variance = np.var(x, axis=-1, keepdims=True)
        self.xivar = np.sqrt(self.variance + self.eps)
        x_normalized = self.x / self.xivar
        output = gamma * x_normalized
        return output


    def backward(self, gy):
        x = self.x
        xmu = self.x
        xivar = self.xivar
        gamma = self.gamma
        dout = gy

        N, _, D= x.shape
        
        dgamma = (dout*xmu/xivar).sum(axis=0,keepdims=False).sum(axis=0,keepdims=False)

        dlxhat = dout*gamma
        dxhatx = 1/xivar
        dlvar = -0.5*((gamma*xmu*xivar**(-3)*dout).sum(axis=-1,keepdims=True))
        dlvarx = 2*xmu/D
        dlmu = -1.*((dlxhat/xivar).sum(axis=-1,keepdims=True))-2.*((dlvar*xmu).sum(axis=-1,keepdims=True)/D)


        dx = dlxhat*dxhatx + dlvar*dlvarx + dlmu/D
        return dx, dgamma


class Dropout(NumpyKernel):
    def __init__(self, dropout_ratio):
        self.dropout_ratio = dropout_ratio

    def forward(self, x):
        if Config.train:
            mask = np.random.rand(*x.shape) > self.dropout_ratio
            self.mask = mask
            scale = np.array(1.0 - self.dropout_ratio).astype(x.dtype)
            y = x * mask / scale
            return y
        else:
            return (1-self.dropout_ratio)*x

    def backward(self, gy):
        gx = np.where(self.mask, gy, 0)
        return gx



class Conv2d(NumpyKernel):
    def __init__(self, stride=1, pad=0):
        super().__init__()
        self.stride = pair(stride)
        self.pad = pair(pad)

    def forward(self, x, W, b):
        #xp = cuda.get_array_module(x)

        KH, KW = W.shape[2:]
        col = im2col_array(x, (KH, KW), self.stride, self.pad, to_matrix=False)

        y = np.tensordot(col, W, ((1, 2, 3), (1, 2, 3)))
        if b is not None:
            y += b
        y = np.rollaxis(y, 3, 1)
        # y = np.transpose(y, (0, 3, 1, 2))
        return y

    def backward(self, gy):
        x, W, b = self.inputs
        # ==== gx ====
        gx = Deconv2d(stride=self.stride, pad=self.pad,
                      outsize=(x.shape[2], x.shape[3]))(gy, W, None)
        # ==== gW ====
        gW = Conv2DGradW(self)(x, gy)
        # ==== gb ====
        gb = None
        if b.data is not None:
            gb = gy.sum(axis=(0, 2, 3))
        return gx, gW, gb



class Deconv2d(NumpyKernel):
    def __init__(self, stride=1, pad=0, outsize=None):
        super().__init__()
        self.stride = pair(stride)
        self.pad = pair(pad)
        self.outsize = outsize

    def forward(self, x, W, b):
        #xp = cuda.get_array_module(x)

        Weight = W
        SH, SW = self.stride
        PH, PW = self.pad
        C, OC, KH, KW = Weight.shape
        N, C, H, W = x.shape
        if self.outsize is None:
            out_h = get_deconv_outsize(H, KH, SH, PH)
            out_w = get_deconv_outsize(W, KW, SW, PW)
        else:
            out_h, out_w = pair(self.outsize)
        img_shape = (N, OC, out_h, out_w)

        gcol = np.tensordot(Weight, x, (0, 1))
        gcol = np.rollaxis(gcol, 3)
        y = col2im_array(gcol, img_shape, (KH, KW), self.stride, self.pad,
                         to_matrix=False)
        # b, k, h, w
        if b is not None:
            self.no_bias = True
            y += b.reshape((1, b.size, 1, 1))
        return y

    def backward(self, gy):
        x, W, b = self.inputs

        # ==== gx ====
        gx = Conv2d(stride=self.stride, pad=self.pad)(gy, W, None)
        # ==== gW ====
        f = Conv2DGradW(self)
        gW = f(gy, x)
        # ==== gb ====
        gb = None
        if b.data is not None:
            gb = gy.sum(axis=(0, 2, 3))
        return gx, gW, gb


class Conv2DGradW(NumpyKernel):
    def __init__(self, conv2d):
        W = conv2d.inputs[1]
        kh, kw = W.shape[2:]
        self.kernel_size = (kh, kw)
        self.stride = conv2d.stride
        self.pad = conv2d.pad

    def forward(self, x, gy):
        #xp = cuda.get_array_module(x)

        col = im2col_array(x, self.kernel_size, self.stride, self.pad,
                           to_matrix=False)
        gW = np.tensordot(gy, col, ((0, 2, 3), (0, 4, 5)))
        return gW

    def backward(self, gys):
        x, gy = self.inputs
        gW, = self.outputs

        xh, xw = x.shape[2:]
        gx = Deconv2d(stride=self.stride, pad=self.pad,
                      outsize=(xh, xw))(gy, gW)
        ggy = Conv2d(stride=self.stride, pad=self.pad)(x, gW)
        return gx, ggy


class Pooling(NumpyKernel):
    def __init__(self, kernel_size, stride=1, pad=0):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.pad = pad

    def forward(self, x):
        col = im2col_array(x, self.kernel_size, self.stride, self.pad,
                           to_matrix=False)

        N, C, KH, KW, OH, OW = col.shape
        col = col.reshape((N, C, KH * KW, OH, OW))
        self.indexes = col.argmax(axis=2)
        y = col.max(axis=2)
        return y

    def backward(self, gy):
        return Pooling2DGrad(self)(gy)


class Pooling2DGrad(NumpyKernel):
    def __init__(self, mpool2d):
        self.mpool2d = mpool2d
        self.kernel_size = mpool2d.kernel_size
        self.stride = mpool2d.stride
        self.pad = mpool2d.pad
        self.input_shape = mpool2d.inputs[0].shape
        self.dtype = mpool2d.inputs[0].dtype
        self.indexes = mpool2d.indexes

    def forward(self, gy):
        #xp = cuda.get_array_module(gy)

        N, C, OH, OW = gy.shape
        N, C, H, W = self.input_shape
        KH, KW = pair(self.kernel_size)

        gcol = np.zeros((N * C * OH * OW * KH * KW), dtype=self.dtype)

        indexes = (self.indexes.ravel()
                   + np.arange(0, self.indexes.size * KH * KW, KH * KW))
        
        gcol[indexes] = gy.ravel()
        gcol = gcol.reshape(N, C, OH, OW, KH, KW)
        gcol = np.swapaxes(gcol, 2, 4)
        gcol = np.swapaxes(gcol, 3, 5)

        gx = col2im_array(gcol, (N, C, H, W), self.kernel_size, self.stride,
                          self.pad, to_matrix=False)
        return gx

    def backward(self, ggx):
        f = Pooling2DWithIndexes(self.mpool2d)
        return f(ggx)


class Pooling2DWithIndexes(NumpyKernel):
    def __init__(self, mpool2d):
        self.kernel_size = mpool2d.kernel_size
        self.stride = mpool2d.stride
        self.pad = mpool2d.pad
        self.input_shpae = mpool2d.inputs[0].shape
        self.dtype = mpool2d.inputs[0].dtype
        self.indexes = mpool2d.indexes

    def forward(self, x):
        col = im2col_array(x, self.kernel_size, self.stride, self.pad,
                           to_matrix=False)
        N, C, KH, KW, OH, OW = col.shape
        col = col.reshape(N, C, KH * KW, OH, OW)
        col = col.transpose(0, 1, 3, 4, 2).reshape(-1, KH * KW)
        indexes = self.indexes.ravel()
        col = col[np.arange(len(indexes)), indexes]
        return col.reshape(N, C, OH, OW)



class AveragePooling(NumpyKernel):
    def __init__(self, kernel_size, stride=1, pad=0):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.pad = pad
        self.input_shape = None

    def forward(self, x):
        self.input_shape = x.shape
        col = im2col_array(x, self.kernel_size, self.stride, self.pad,
                           to_matrix=False)
        y = col.mean(axis=(2, 3))
        return y

    def backward(self, gy):
        # TODO(Koki): This is simple implementation
        N, C, OH, OW = gy.shape
        KW, KH = pair(self.kernel_size)
        gy /= (KW*KH)
        gcol = np.broadcast_to(gy.reshape(-1), (KH, KW, N*C*OH*OW))
        gcol = gcol.reshape((KH, KW, N, C, OH, OW)).transpose((2, 3, 0, 1, 4, 5))
        gx = Col2im(self.input_shape, self.kernel_size, self.stride,
                    self.pad, False)(gcol)
        return gx


class Im2col(NumpyKernel):
    def __init__(self, kernel_size, stride, pad, to_matrix):
        super().__init__()
        self.input_shape = None
        self.kernel_size = kernel_size
        self.stride = stride
        self.pad = pad
        self.to_matrix = to_matrix

    def forward(self, x):
        self.input_shape = x.shape
        y = im2col_array(x, self.kernel_size, self.stride, self.pad,
                         self.to_matrix)
        return y

    def backward(self, gy):
        gx = Col2im(self.input_shape, self.kernel_size, self.stride,
                    self.pad, self.to_matrix)(gy)
        return gx


class Col2im(NumpyKernel):
    def __init__(self, input_shape, kernel_size, stride, pad, to_matrix):
        super().__init__()
        self.input_shape = input_shape
        self.kernel_size = kernel_size
        self.stride = stride
        self.pad = pad
        self.to_matrix = to_matrix

    def forward(self, x):
        y = col2im_array(x, self.input_shape, self.kernel_size, self.stride,
                         self.pad, self.to_matrix)
        return y

    def backward(self, gy):
        gx = Im2col(self.kernel_size, self.stride, self.pad,
                    self.to_matrix)(gy)
        return gx


class MeanSquaredError(NumpyKernel):
    def forward(self, x0, x1):
        diff = x0 - x1
        y = (diff ** 2).sum() / len(diff)
        return y

    def backward(self, gy):
        x0, x1 = self.xs[0], self.xs[1]
        diff = x0 - x1
        gy = np.broadcast_to(gy, diff.shape)
        gx0 = gy * diff * (2. / len(diff))
        gx1 = -gx0
        return gx0, gx1


class SoftmaxCrossEntropy(NumpyKernel):
    def forward(self, x, t):
        N = x.shape[0]
        log_z = logsumexp(x, axis=1)
        log_p = x - log_z
        log_p = log_p[np.arange(N), t.ravel()]
        y = -log_p.sum() / np.float32(N)
        return y

    def backward(self, gy):
        x, t = self.xs
        N, CLS_NUM = x.shape
        gy *= 1/N
        y = softmax(x, axis=-1)
        # convert to one-hot
        t_onehot = np.eye(CLS_NUM, dtype=t.dtype)[t]
        y = (y - t_onehot) * gy
        return y
