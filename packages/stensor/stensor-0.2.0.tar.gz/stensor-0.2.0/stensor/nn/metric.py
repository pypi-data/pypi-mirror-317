
def accuracy(y, t):
    y, t = y.data, t.data

    pred = y.argmax(axis=1).reshape(t.shape)
    result = (pred == t)
    acc = result.mean()
    return acc


__all__=["accuracy"]