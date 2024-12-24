from dataclasses import dataclass
from typing import Literal

@dataclass
class GPTConfig:
    '''

    '''
    batch_size: int = 16
    # embedding:
    vocab_size: int = 6400
    hidden_size: int = 512
    max_seq_len: int = 512
    init_std: float = 0.5
    norm: str = None
    emb_dropout_rate: float = 0.0
    # position:
    position_type: str = 'rope'
    max_size: int = 512
    rope_base: float = 10000.0
    expand_type: str = None
    use_rope: bool = False
    no_use_cached_emb: bool = True
    # blocks:
    num_layers: int = 8 # 2 noop layers
    init_st: float = 0.00066
    sandwich_norm: bool = True
    #  layernorm:
    norm_type: str = 'RMSNorm'
    norm_epsilon: float = 1e-5
    #  attention:
    attention_type: Literal['MHA', 'GQA', 'MQA'] = 'GQA'
    num_heads: int = 4
    kv_group_size: int = 2
    flash_attn: bool = False
    attn_qkv_bias: bool = False
    attn_scores_dropout_rate: float = 0.0
    attn_projection_bias: bool = False
    attn_projection_dropout_rate: float = 0.0
    attn_post_norm_scale: float = 0.0292
    #  ffn:
    use_moe: bool = False
    mlp_hidden_size: int = 0
    mlp_times: int = 64
    mlp_activation: Literal['swiglu', 'silu', 'relu'] = 'silu'
    mlp_dropout_rate: float = 0.0
    mlp_bias: bool = False
    mlp_post_norm_scale: float = 0.0446
    # head:
    shared_embedding: bool = False 
    # loss:
    cross_entropy_reduction: Literal['sum', 'mean', 'none'] = 'none'
