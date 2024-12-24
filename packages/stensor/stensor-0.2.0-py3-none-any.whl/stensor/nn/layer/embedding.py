import numpy as np

from stensor.nn.module import Module
from stensor.common import Parameter


class Embedding(Module):
    r"""
    Embedding layer.
    Retrieve the word embeddings in weight stored in the layer using indices specified in `input`.

    Args:
        num_embeddings (int): Size of the dictionary of embeddings.
        embedding_dim (int): The size of each embedding vector.
        weight_init (string) :Initialization method for embedding table,must be 'normal' or 'uniform'.
            Default: 'normal'.

    Inputs:
        - **input** (Tensor) - The indices used to lookup in the embedding vector. The data type must be int, 
        and the value should be in range `[0, num_embeddings)`.

    Outputs:
        Tensor, has the same data type as weight, the shape is :math:`(*input.shape, embedding_dim)`.

    """
    def __init__(self, vocab_size, embedding_size, weight_init='normal'):
        super(Embedding, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        if weight_init == 'uniform':
            self.embedding = Parameter(np.random.uniform(-1.0, 1.0, (self.vocab_size, self.embedding_size)))
        elif weight_init == 'normal':
            self.embedding = Parameter(np.random.normal(0.0, 1.0, (self.vocab_size, self.embedding_size)))
        else:
            raise ValueError("Unsupported initialization method. Use 'uniform' or 'normal'.")


    def forward(self, ids):
        out_shape = ids.shape + (self.embedding_size,)  #(*input.shape, embedding_dim)
        out = self.embedding[ids]
        assert out.shape == out_shape
        return out.type_as(self.embedding)
