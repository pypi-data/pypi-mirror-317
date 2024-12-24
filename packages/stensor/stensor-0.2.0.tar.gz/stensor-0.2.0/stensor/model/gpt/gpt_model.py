import math
from typing import Optional
from stensor import Tensor, nn, no_grad
from stensor.ops import functional as F

from .gpt_config import GPTConfig
from .rope import precompute_pos_cis, apply_rotary_emb


class GroupQueryAttention(nn.Module):
    r"""
    Group-Query Attention (GQA) is a variant of Multi-Head Attention (MHA) proposed by Google. 
    It is essentially an optimization method that shares the KV cache.
    """
    def __init__(self, config: GPTConfig):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_heads
        self.head_dim = config.hidden_size // config.num_heads
        self.kv_group_size = config.kv_group_size
        self.q_heads = self.num_heads
        self.kv_heads = self.q_heads // config.kv_group_size

        self.attn_qkv_bias = config.attn_qkv_bias
        self.attn_projection_bias = config.attn_projection_bias
        self.wq = nn.Linear(self.hidden_size, self.head_dim * self.q_heads, bias=self.attn_qkv_bias)
        self.wk = nn.Linear(self.hidden_size, self.head_dim * self.kv_heads, bias=self.attn_qkv_bias)
        self.wv = nn.Linear(self.hidden_size, self.head_dim * self.kv_heads, bias=self.attn_qkv_bias)
        self.wo = nn.Linear(self.head_dim * self.num_heads, self.hidden_size, bias=self.attn_projection_bias)

        self.k_cache, self.v_cache = None, None

        self.attn_scores_dropout_rate = config.attn_scores_dropout_rate
        self.attn_projection_dropout_rate = config.attn_projection_dropout_rate
        self.attn_scores_dropout = nn.Dropout(config.attn_scores_dropout_rate)
        self.attn_projection_dropout = nn.Dropout(config.attn_projection_dropout_rate)
        
        #TODO: support flash attention operation.
        self.flash = config.flash_attn

    def forward(self, x: Tensor, pos_cis, kv_cache=False, mask=None):
        bsz, seqlen, _ = x.shape

        xq, xk, xv = self.wq(x), self.wk(x), self.wv(x)
        xq = xq.view(bsz, seqlen, self.q_heads, self.head_dim)
        xk = xk.view(bsz, seqlen, self.kv_heads, self.head_dim)
        xv = xv.view(bsz, seqlen, self.kv_heads, self.head_dim)

        xq, xk = apply_rotary_emb(xq, xk, pos_cis)
        
        # More efficient implementation for kv_cache in gpt2.
        if kv_cache and not self.training:
            if seqlen == 1 and all(cache is not None for cache in (self.k_cache, self.v_cache)):
                xk = F.concat((self.k_cache, xk), axis=1)
                xv = F.concat((self.v_cache, xv), axis=1)
            self.k_cache, self.v_cache = xk, xv

        xk = F.repeat_interleave(xk, self.kv_group_size, 2)
        xv = F.repeat_interleave(xv, self.kv_group_size, 2)
        
        xq = xq.transpose(1, 2)
        xk = xk.transpose(1, 2)
        xv = xv.transpose(1, 2)
        if self.flash and seqlen != 1:
            output = F.scaled_dot_product_attention(xq, xk, xv, attn_mask=None,
                                                                      dropout_p=self.dropout if self.training else 0.0,
                                                                      is_causal=True)
        else:
            scores = F.matmul(xq, xk.transpose(2, 3)) / math.sqrt(self.head_dim)
            # The mask operation applies only to the autoregressive model training process and the prefill phase during inference. 
            if seqlen != 1:
                scores = scores + mask # (bs, n_local_heads, seqlen, cache_len + seqlen)
            scores = F.softmax(scores.type_as(xq), -1)
            scores = self.attn_scores_dropout(scores)
            output = F.matmul(scores, xv)  # (bs, n_local_heads, seqlen, head_dim)
        output = output.transpose(1, 2).view(bsz, seqlen, -1)
        output = self.attn_projection_dropout(self.wo(output))
        return output


class FFNSwiGLU(nn.Module):
    r"""
    The FFN layer is short for Position-wise Feed-Forward Networks (FFN). 
    1)  The FFN receives a tensor x (a hidden representation of a specific position in the sequence) and processes it 
        through two learnable linear transformations, applying modified linearity (ReLU) activation 
        between the two linear transformations.(Glorot et al.,2011.)
        <https://proceedings.mlr.press/v15/glorot11a/glorot11a.pdf>
    2)  Subsequent studies proposed replacing ReLU with other non-linear activation functions.
        <https://arxiv.org/pdf/1710.05941>
    3)  (Dauphin et al., 2016) proposed a gated linear unit (GLU), defined as the element-by-element product of 
        two input linear transformations, one of which is activated by sigmoid.
        <https://arxiv.org/pdf/1612.08083>
        Variations of other Transformer FFN layers: <https://arxiv.org/pdf/2002.05202>
    4)  The official code provided by LLaMA uses the F.silu() activation function instead of Swish.
    5)  The original FPN layer has only two weight matrices. To keep the number of parameters and 
        the calculation amount constant, the number of hidden units needs to be reduced by 2/3.
    """
    def __init__(self, config: GPTConfig):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.mlp_hidden_size = config.mlp_hidden_size
        if config.mlp_hidden_size == 0:
            self.mlp_times = config.mlp_times
            self.mlp_hidden_size = 4 * self.hidden_size
            self.mlp_hidden_size = int(2 * self.mlp_hidden_size / 3)
            self.mlp_hidden_size = self.mlp_times * ((self.mlp_hidden_size + self.mlp_times - 1) // self.mlp_times)
        self.bais = config.mlp_bias
        if config.mlp_activation == "swiglu":
            self.activation = F.swish
        elif config.mlp_activation == "silu":
            self.activation = F.silu
        elif config.mlp_activation == "relu":
            self.activation = F.relu
        self.w1 = nn.Linear(self.hidden_size, self.mlp_hidden_size, bias=self.bais)
        self.w2 = nn.Linear(self.mlp_hidden_size, self.hidden_size, bias=self.bais)
        self.w3 = nn.Linear(self.hidden_size, self.mlp_hidden_size, bias=self.bais)
        self.dropout = nn.Dropout(config.mlp_dropout_rate)

    def forward(self, x):
        return self.dropout(self.w2(self.activation(self.w1(x)) * self.w3(x)))


class TransformerBlock(nn.Module):
    def __init__(self, layer_id: int, config: GPTConfig):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.attention_norm = nn.RMSNorm(config.hidden_size, eps=config.norm_epsilon)
        self.attention = GroupQueryAttention(config)
        self.ffn_norm = nn.RMSNorm(config.hidden_size, eps=config.norm_epsilon)
        if config.use_moe:
            self.feed_forward = MOEFeedForward(config)
        else:
            self.feed_forward = FFNSwiGLU(config)

    def forward(self, x: Tensor, pos_cis, kv_cache: bool = False, mask: Optional[Tensor] = None): 
        h = x + self.attention(self.attention_norm(x), pos_cis, kv_cache, mask)
        out = h + self.feed_forward(self.ffn_norm(h))
        return out


class GPTModel(nn.Module):
    """A generative pre-trained transformer language model under decoder-only framework, 
    such as the GPT-3(175B) which are developed by OpenAI and the LLama3(70B) model which are developed by Meta.

    Args:
        config (GPTConfig): Transformer config
    """
    def __init__(self, config: GPTConfig) -> None:
        super().__init__()
        self.config = config

        self.tok_embeddings = nn.Embedding(config.vocab_size, config.hidden_size)
        self.dropout = nn.Dropout(config.emb_dropout_rate)
        self.layers = nn.ModuleList()
        for layer_id in range(config.num_layers):
            self.layers.append(TransformerBlock(layer_id, config))

        self.norm = nn.RMSNorm(config.hidden_size, eps=config.norm_epsilon)
        self.output = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        
        # Shared Parameters
        self.tok_embeddings.embedding = self.output.W
        
        self.softmax_cross_entropy = nn.SoftmaxCrossEntropy(reduction=config.cross_entropy_reduction)
        self.pos_cis = precompute_pos_cis(config.hidden_size // config.num_heads, config.max_seq_len)

    def forward(self, tokens: Tensor = None, targets: Tensor = None, kv_cache=False, loss_mask=None, **keyconfig):
        current_idx = 0
        if 'input_ids' in keyconfig:
            tokens = keyconfig['input_ids']
        if 'attention_mask' in keyconfig:
            targets = keyconfig['attention_mask']
        if 'current_idx' in keyconfig:
            current_idx = int(keyconfig['current_idx'])
        if 'loss_mask' in keyconfig:
            loss_mask = keyconfig['loss_mask']
            
        _bsz, seqlen = tokens.shape  # [_bsz, seqlen]
        h = self.tok_embeddings(tokens) # [_bsz, seqlen, config.hidden_size]
        h = self.dropout(h)
        pos_cis = self.pos_cis[current_idx:current_idx + seqlen]
        
        mask = None
        #The mask operation applies only to the autoregressive model training process and the prefill phase during inference.
        if seqlen > 1:
            mask = F.full((1, 1, seqlen, seqlen), float("-inf"))
            mask = F.triu(mask, diagonal=1)
            # TODO: More efficient implementation.
            # mask = F.tril(F.ones([seqlen, seqlen]))
            # masked_scores = scores.masked_fill(mask == 0, float('-inf'))
            mask.requires_grad = False
            if not self.training and kv_cache and current_idx != 0:
                # When performing key-value caching, we compute the attention scores
                # only for the new sequence. Thus, the matrix of scores is of size
                # (seqlen, cache_len + seqlen), and the only masked entries are (i, j) for
                # j > cache_len + i, since row i corresponds to token cache_len + i.
                mask = F.cat([F.zeros((seqlen, current_idx), device=tokens.device), mask], dim=1).type_as(h)     
        for layer in self.layers:
            h = layer(h, pos_cis, kv_cache, mask)

        h = self.norm(h)
        logits = self.output(h)
        logits = logits.view(-1, logits.shape[-1])
        
        loss = None
        if targets is not None:
            loss = self.softmax_cross_entropy(logits, targets.view(-1))
            if loss_mask is not None:
                loss_mask = loss_mask.view(-1).type_as(loss)
                loss = F.sum(loss * loss_mask) / loss_mask.sum()     
       
        return logits, loss

    @no_grad()
    def generate(self, idx, eos, max_new_tokens, temperature=0.7, top_k=8, rp=1., stream=True, kv_cache=True):
        r"""
        The generative reasoning process of a typical autoregressive model consists of two stages:

        Prefill phase: Enter a prompt sequence to generate the key cache and value cache (KV cache) for each transformer layer. 
                       This phase can take full advantage of parallel computing.
        Decoding phase: The KV cache is used and updated to generate words one by one (no parallelism). 
                        The generated words depend on the words that have been generated before. 
                        The inference calculation in this phase consists of two parts: 
                        updating the KV cache and calculating the output of decoder layers.

        Args:
            idx: the input data profill need to infer.
            eos: The generation process terminates when the maximum number of tokens max_new_tokens is reached 
                 or the end marker eos is encountered.
            temperature: The temperature sampling parameter controls the randomness of the generation. 
                         The higher the temperature, the more random the text is generated. 
                         When the temperature is 0, the token with the highest probability is selected.
            top_k: The top_k sampling parameter is used to limit the number of tokens considered in each sampling. 
                    Only the top_k tokens with the highest probability are sampled.
            rp: The Repeated penalty parameter is used to punish the generated token to prevent duplicate content from being generated.
            stream: The stream parameter is used to control whether to output the generated text fragments in streaming mode.
            kv_cache: The kv_cache parameter is used to determine whether to use the cache mechanism to improve the generation efficiency.
        """
        index = idx.shape[1]
        init_inference = True
        while idx.shape[1] < max_new_tokens - 1:
            if init_inference or not kv_cache:
                # The GQA module generates KV key-value pairs and stores them in the KV cache during the Prefill phase.
                inference_res, init_inference = self(idx, kv_cache=kv_cache), False
            else:
                inference_res = self(idx[:, -1:], kv_cache=kv_cache, current_idx=idx.shape[1] - 1)
            logits = inference_res[0][-1,:]

            # rp: repetition_penalty
            if rp != 1.:
                for token in set(idx.data.reshape(-1,).tolist()):
                    logits.data[token] = logits.data[token] / rp

            logits = logits / temperature
            if top_k == 1:
                _, idx_next = F.max(logits, axis=-1, keepdims=False)
            else:
                topk_values, topk_indices = F.topk(logits, min(top_k, logits.shape[-1]))
                sample_idx = F.multinomial(topk_values, num_samples=1)
                idx_next = topk_indices[sample_idx]

            if idx_next.data == eos:
                break

            idx = F.concat((idx, idx_next.view(1,1)), axis=-1)

            if stream:
                yield idx[:, index:]

        if not stream:
            yield idx[:, index:]

    @no_grad()
    def eval_one(self, idx):
        r"""
        Generate one token for unit tests.
        """
        idx_cond = idx if idx.shape[1] <= self.config.max_seq_len else idx[:, -self.config.max_seq_len:]
        inference_res = self(idx_cond)
        logits = inference_res[0]
        _, idx = F.max(logits, axis=-1, keepdims=False)
        return logits, idx
