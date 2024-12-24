import math
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np

from stensor import Tensor, nn
from stensor.ops import functional as F


# prompt = "the answer to the ultimate question of life, the universe, and everything is "
# # 128000对应token为<|begin_of_text|>，用来标记文本的开始
# tokens = np.array([128000, 1820, 4320, 311, 279, 17139, 3488, 315, 2324, 11, 279, 15861, 11, 323, 4395, 374, 220])
# print(tokens)
# tokens = Tensor(tokens)
# print(tokens)

# token_embeddings_unnormalized = nn.Embedding(128256, 4096)(tokens)
# print(token_embeddings_unnormalized.shape)


@dataclass
class LlamaConfig:
    #dim: int = 4096
    dim: int = 16 #256
    #n_layers: int = 32
    n_layers: int = 8
    #n_heads: int = 32
    n_heads: int = 1
    n_kv_heads: Optional[int] = None
    vocab_size: int = 2
    multiple_of: int = 256  # make SwiGLU hidden layer size multiple of large power of 2
    ffn_dim_multiplier: Optional[float] = None
    norm_eps: float = 1e-5
    rope_theta: float = 500000

    max_batch_size: int = 32
    max_seq_len: int = 2048


def precompute_freqs_cis(dim: int, end: int, theta: float = 10000.0):
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))
    t = torch.arange(end, device=freqs.device, dtype=torch.float32)
    freqs = torch.outer(t, freqs)
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs)  # complex64
    return freqs_cis


def reshape_for_broadcast(freqs_cis: Tensor, x: Tensor):
    ndim = x.ndim
    assert 0 <= 1 < ndim
    assert freqs_cis.shape == (x.shape[1], x.shape[-1])
    shape = [d if i == 1 or i == ndim - 1 else 1 for i, d in enumerate(x.shape)]
    return freqs_cis.view(*shape)


def apply_rotary_emb(
    xq: Tensor,
    xk: Tensor,
    freqs_cis: Tensor,
) -> Tuple[Tensor, Tensor]:
    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))
    freqs_cis = reshape_for_broadcast(freqs_cis, xq_)
    xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(3)
    xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(3)
    return xq_out.type_as(xq), xk_out.type_as(xk)


# def repeat_kv(x: Tensor, n_rep: int) -> Tensor:
#     """torch.repeat_interleave(x, dim=2, repeats=n_rep)"""
#     bs, slen, n_kv_heads, head_dim = x.shape
#     if n_rep == 1:
#         return x
#     return (
#         x[:, :, :, None, :]
#         .expand(bs, slen, n_kv_heads, n_rep, head_dim)
#         .reshape(bs, slen, n_kv_heads * n_rep, head_dim)
#     )


class Attention(nn.Module):
    def __init__(self, args: LlamaConfig):
        super().__init__()
        self.n_kv_heads = args.n_heads if args.n_kv_heads is None else args.n_kv_heads
        self.n_local_heads = args.n_heads
        self.n_local_kv_heads = self.n_kv_heads
        self.n_rep = self.n_local_heads // self.n_local_kv_heads
        self.head_dim = args.dim // args.n_heads

        self.wq = nn.Linear(args.dim, args.n_heads * self.head_dim,bias=False,)
        self.wk = nn.Linear(args.dim, self.n_kv_heads * self.head_dim, bias=False,)
        self.wv = nn.Linear(args.dim, self.n_kv_heads * self.head_dim, bias=False,)
        self.wo = nn.Linear(args.n_heads * self.head_dim, args.dim,bias=False,)

        # self.cache_k = torch.zeros(
        #     (
        #         args.max_batch_size,
        #         args.max_seq_len,
        #         self.n_local_kv_heads,
        #         self.head_dim,
        #     )
        # )
        # self.cache_v = torch.zeros(
        #     (
        #         args.max_batch_size,
        #         args.max_seq_len,
        #         self.n_local_kv_heads,
        #         self.head_dim,
        #     )
        # )

    def forward(
        self,
        x: Tensor,
        # start_pos: int,
        # freqs_cis: Optional[Tensor],
        # mask: Optional[Tensor],
    ):  
        bsz, seqlen, _ = x.shape
        xq, xk, xv = self.wq(x), self.wk(x), self.wv(x)

        xq = xq.view(bsz, seqlen, self.n_local_heads, self.head_dim)
        xk = xk.view(bsz, seqlen, self.n_local_kv_heads, self.head_dim)
        xv = xv.view(bsz, seqlen, self.n_local_kv_heads, self.head_dim)
        #TODO:
        #xq, xk = apply_rotary_emb(xq, xk, freqs_cis=freqs_cis)

        # self.cache_k = self.cache_k.to(xq)
        # self.cache_v = self.cache_v.to(xq)

        # self.cache_k[:bsz, start_pos : start_pos + seqlen] = xk
        # self.cache_v[:bsz, start_pos : start_pos + seqlen] = xv

        # keys = self.cache_k[:bsz, : start_pos + seqlen]
        # values = self.cache_v[:bsz, : start_pos + seqlen]

        #print(xq.shape,xk.shape,xv.shape) #torch.Size([1, 2, 1, 4]) torch.Size([1, 2, 1, 4]) torch.Size([1, 2, 1, 4])
        #print(keys.shape, values.shape) #torch.Size([1, 2, 1, 4]) torch.Size([1, 2, 1, 4])
        keys = xk
        values = xv

        # # repeat k/v heads if n_kv_heads < n_heads
        # keys = repeat_kv(
        #     keys, self.n_rep
        # )  # (bs, cache_len + seqlen, n_local_heads, head_dim)
        # values = repeat_kv(
        #     values, self.n_rep
        # )  # (bs, cache_len + seqlen, n_local_heads, head_dim)

        xq = xq.transpose(1, 2)  # (bs, n_local_heads, seqlen, head_dim)
        keys = keys.transpose(1, 2)  # (bs, n_local_heads, cache_len + seqlen, head_dim)
        values = values.transpose(
            1, 2
        )  # (bs, n_local_heads, cache_len + seqlen, head_dim)
        scores = F.matmul(xq, keys.transpose(2, 3)) / math.sqrt(self.head_dim)
        mask = Tensor(np.array([[0., -1e9], [0., 0.]]))
        scores = scores + mask
        # if mask is not None:
        #     scores = scores + mask  # (bs, n_local_heads, seqlen, cache_len + seqlen)
        scores = F.softmax(scores, axis=-1)
        output = F.matmul(scores, values)  # (bs, n_local_heads, seqlen, head_dim)
        output = output.transpose(1, 2).view(bsz, seqlen, -1)
        return self.wo(output)


class FeedForward(nn.Module):
    def __init__(
        self,
        dim: int,
        hidden_dim: int,
        multiple_of: int,
        ffn_dim_multiplier: Optional[float],
    ):
        super().__init__()
        hidden_dim = int(2 * hidden_dim / 3)
        # custom dim factor multiplier
        if ffn_dim_multiplier is not None:
            hidden_dim = int(ffn_dim_multiplier * hidden_dim)
        hidden_dim = multiple_of * ((hidden_dim + multiple_of - 1) // multiple_of)

        self.w1 = nn.Linear(
            dim, hidden_dim, bias=False
        )
        self.w2 = nn.Linear(
            hidden_dim, dim, bias=False
        )
        self.w3 = nn.Linear(
            dim, hidden_dim, bias=False
        )

    def forward(self, x):
        return self.w2(F.relu(self.w1(x)) * self.w3(x))


class TransformerBlock(nn.Module):
    def __init__(self, layer_id: int, args: LlamaConfig):
        super().__init__()
        self.n_heads = args.n_heads
        self.dim = args.dim
        self.head_dim = args.dim // args.n_heads
        self.attention = Attention(args)
        self.feed_forward = FeedForward(
            dim=args.dim,
            hidden_dim=4 * args.dim,
            multiple_of=args.multiple_of,
            ffn_dim_multiplier=args.ffn_dim_multiplier,
        )
        self.layer_id = layer_id
        self.attention_norm = nn.RMSNorm(args.dim, eps=args.norm_eps)
        self.ffn_norm = nn.RMSNorm(args.dim, eps=args.norm_eps)


    def forward(
        self,
        x: Tensor,
        # start_pos: int,
        # freqs_cis: Tensor,
        # mask: Optional[Tensor],
    ):  
        h = x + self.attention(self.attention_norm(x))
        out = h + self.feed_forward(self.ffn_norm(h))
        return out


class Llama(nn.Module):
    def __init__(self, params: LlamaConfig):
        super().__init__()
        self.params = params
        self.vocab_size = params.vocab_size
        self.n_layers = params.n_layers

        self.tok_embeddings = nn.Embedding(
            params.vocab_size, params.dim
        )

        self.layers = nn.ModuleList()
        for layer_id in range(params.n_layers):
            self.layers.append(TransformerBlock(layer_id, params))

        self.norm = nn.RMSNorm(params.dim, eps=params.norm_eps)
        self.output = nn.Linear(
            params.dim, params.vocab_size, bias=False
        )

        # self.freqs_cis = precompute_freqs_cis(
        #     params.dim // params.n_heads,
        #     params.max_seq_len * 2,
        #     params.rope_theta,
        # )

    #@torch.inference_mode()
    def forward(self, tokens: Tensor):
        _bsz, seqlen = tokens.shape
        h = self.tok_embeddings(tokens)
        # self.freqs_cis = self.freqs_cis.to(h.device)
        # freqs_cis, mask = None, None
        # freqs_cis = self.freqs_cis[start_pos : start_pos + seqlen]

        # mask = None
        # if seqlen > 1:
        #     import torch
        #     tokens = torch.tensor(np.array([[0,0],[1,1]]))
        #     mask = torch.full((seqlen, seqlen), float("-inf"), device=tokens.device)

        #     mask = torch.triu(mask, diagonal=1)

        #     # When performing key-value caching, we compute the attention scores
        #     # only for the new sequence. Thus, the matrix of scores is of size
        #     # (seqlen, cache_len + seqlen), and the only masked entries are (i, j) for
        #     # j > cache_len + i, since row i corresponds to token cache_len + i.
        #     mask = torch.hstack(
        #         [torch.zeros((seqlen, 0), device=tokens.device), mask]
        #     )
        #     print(mask)

        for layer in self.layers:
            h = layer(h)
        h = self.norm(h)
        output = self.output(h).float()
        return output.view(-1, output.shape[-1]) 
