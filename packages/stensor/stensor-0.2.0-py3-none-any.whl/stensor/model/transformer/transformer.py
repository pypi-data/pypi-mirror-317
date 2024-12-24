

import numpy as np
from stensor import nn
from stensor.ops import functional as F
from stensor.common import Tensor, Parameter


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000): 
        super(PositionalEncoding, self).__init__()
        self.d_model = d_model
        self.dropout = dropout
        pe = np.zeros((max_len, d_model))
        pos = np.arange(0, max_len)
        pos = pos[:, np.newaxis]
        div_term = pos / pow(10000.0, np.arange(0, d_model, 2) / d_model)
        pe[:, 0::2] = np.sin(div_term)
        pe[:, 1::2] = np.cos(div_term)
        pe = np.expand_dims(pe, axis=0)
        self.pe = Parameter(pe, requires_grad=False)


    def forward(self, x):
        x_pe = F.get_item(self.pe, (slice(0,1,1), slice(0,x.shape[1],1), slice(0,self.d_model,1)))
        x = x + x_pe
        return x


def get_attn_pad_mask(seq_q, seq_k):
    batch_size, len_q = seq_q.shape
    batch_size, len_k = seq_k.shape
    pad_attn_mask = (seq_k == 0).reshape((batch_size, 1, len_k))
    return pad_attn_mask.broadcast_to((batch_size, len_q, len_k))


def get_attn_subsequence_mask(seq):
    attn_shape = [seq.shape[0], seq.shape[1], seq.shape[1]]
    subsequence_mask = np.triu(np.ones(attn_shape), k=1)
    subsequence_mask = Tensor(subsequence_mask) 
    return subsequence_mask 
   

class ScaledDotProductionAttention(nn.Module):
    def __init__(self, d_k):
        super(ScaledDotProductionAttention, self).__init__()
        self.d_k =d_k


    def forward(self, Q, K, V, attn_mask):
        scores = F.matmul(Q, K.transpose(-1, -2)) / np.sqrt(self.d_k)  # scores: [batch_size, n_heads, len_q, len_k]
        scores = scores.masked_fill(attn_mask, -1e9)
        attn = F.softmax(scores, axis=-1)  # attn: [batch_size, n_heads, len_q, len_k]
        context = F.matmul(attn, V)  # context: [batch_size, n_heads, len_q, d_v]
        return context # context: [batch_size, n_heads, len_q, d_v]


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, nhead, bias):
        super(MultiHeadAttention, self).__init__()
        self.nhead = nhead
        self.d_k = int(d_model / nhead)
        self.d_v = int(d_model / nhead)
        self.W_Q = nn.Linear(d_model, d_model, bias=bias)
        self.W_K = nn.Linear(d_model, d_model, bias=bias)
        self.W_V = nn.Linear(d_model, d_model, bias=bias)
        self.concat = nn.Linear(d_model, d_model, bias=bias)
        self.attention = ScaledDotProductionAttention(self.d_k)


    def forward(self, input_Q, input_K, input_V, attn_mask):
        residual, batch_size, len_q = input_Q, input_Q.shape[0], input_Q.shape[1]
        Q = self.W_Q(input_Q).reshape((batch_size, -1, self.nhead, self.d_k)).transpose(1, 2) # Q: [batch_size, n_heads, len_q, d_k]
        K = self.W_K(input_K).reshape((batch_size, -1, self.nhead, self.d_k)).transpose(1, 2) # K: [batch_size, n_heads, len_k, d_k]
        V = self.W_V(input_V).reshape((batch_size, -1, self.nhead, self.d_v)).transpose(1, 2) # V: [batch_size, n_heads, len_v(=len_k), d_v]
        attn_mask = attn_mask.unsqueeze(1).repeat((1, self.nhead, 1, 1))  # attn_mask: [batch_size, n_heads, seq_len, seq_len]
        context = self.attention(Q, K, V, attn_mask) # context: [batch_size, n_heads, len_q, d_v]
        tuple_tensor=[]
        for i in range(self.nhead):
            ans = F.get_item(context, (slice(0,batch_size,1), slice(i,i+1,1), slice(0,len_q,1), slice(0,self.d_v,1)))
            ans = ans.reshape((batch_size, len_q, self.d_v))
            tuple_tensor.append(ans)
        context = F.concat(tuple_tensor, axis=-1) # [batch_size, n_heads, len_q, d_model]
        output = self.concat(context)  # [batch_size, len_q, d_model]
        return nn.LayerNorm()(output + residual)  # output: [batch_size, len_q, d_model]


class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, dim_feedforward, activation, layer_norm_eps, bias):
        super(PositionwiseFeedForward, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(d_model, dim_feedforward, bias=bias),
            activation(),
            nn.Linear(dim_feedforward, d_model, bias=bias)
        )
        self.ln = nn.RMSNorm(normalized_shape=d_model, eps=layer_norm_eps)

    def forward(self, inputs):
        residual = inputs
        output = self.fc(inputs)
        return self.ln(residual + output) # return： [batch_size, seq_len, d_model] 形状不变


class EncoderLayer(nn.Module):
    def __init__(self, d_model, nhead, dim_feedforward, activation, layer_norm_eps, bias):
        super(EncoderLayer, self).__init__()
        self.enc_self_attn = MultiHeadAttention(d_model, nhead, bias)
        self.pos_ffn = PositionwiseFeedForward(d_model, dim_feedforward, activation, layer_norm_eps, bias)

    def forward(self, enc_inputs, enc_self_attn_mask):
        enc_ouputs = self.enc_self_attn(enc_inputs, enc_inputs, enc_inputs, enc_self_attn_mask) # enc_ouputs: [batch_size, src_len, d_model]
        enc_ouputs = self.pos_ffn(enc_ouputs) # enc_outputs: [batch_size, src_len, d_model]
        return enc_ouputs  # enc_outputs: [batch_size, src_len, d_model]


class Encoder(nn.Module):
    def __init__(self, d_model, nhead, num_encoder_layers, dim_feedforward, src_vocab_size,
                dropout, activation, layer_norm_eps, bias):
        super(Encoder, self).__init__()
        self.src_emb = nn.Embedding(src_vocab_size, d_model)
        self.pos_emb = PositionalEncoding(d_model, dropout)
        self.layers = nn.ModuleList([EncoderLayer(d_model, nhead, dim_feedforward, activation, layer_norm_eps, bias) for _ in range(num_encoder_layers)])

    def forward(self, enc_inputs):
        enc_outputs = self.src_emb(enc_inputs) # [batch_size, src_len] -> [batch_size, src_len, d_model]
        enc_outputs = self.pos_emb(enc_outputs) # enc_outputs: [batch_size, src_len, d_model]
        enc_self_attn_mask = get_attn_pad_mask(enc_inputs, enc_inputs)  # enc_self_attn_mask: [batch_size, src_len, src_len]
        for layer in self.layers:
            enc_outputs = layer(enc_outputs, enc_self_attn_mask)
        return enc_outputs  # enc_outputs: [batch_size, src_len, d_model]


class DecoderLayer(nn.Module):
    def __init__(self, d_model, nhead, dim_feedforward, activation, layer_norm_eps, bias):
        super(DecoderLayer, self).__init__()
        self.dec_self_attn = MultiHeadAttention(d_model, nhead, bias)
        self.dec_enc_attn = MultiHeadAttention(d_model, nhead, bias)
        self.pos_ffn = PositionwiseFeedForward(d_model, dim_feedforward, activation, layer_norm_eps, bias)

    def forward(self, dec_inputs, enc_outputs, dec_self_attn_mask, dec_enc_attn_mask):
        dec_outputs = self.dec_self_attn(dec_inputs, dec_inputs, dec_inputs, dec_self_attn_mask)
        dec_outputs = self.dec_enc_attn(dec_outputs, enc_outputs, enc_outputs, dec_enc_attn_mask)
        dec_outputs = self.pos_ffn(dec_outputs)
        return dec_outputs # dec_outputs: [batch_size, tgt_len, d_model]


class Decoder(nn.Module):
    def __init__(self, d_model, nhead, num_decoder_layers, dim_feedforward, tgt_vocab_size, 
                dropout, activation, layer_norm_eps, bias):
        super(Decoder, self).__init__()
        self.tgt_emb = nn.Embedding(tgt_vocab_size, d_model)
        self.pos_emb = PositionalEncoding(d_model, dropout)
        self.layers = nn.ModuleList([DecoderLayer(d_model, nhead, dim_feedforward, activation, layer_norm_eps, bias) for _ in range(num_decoder_layers)])


    def forward(self, dec_inputs, enc_inputs, enc_outputs):
        dec_outputs = self.tgt_emb(dec_inputs)
        dec_outputs = self.pos_emb(dec_outputs)
        dec_self_attn_pad_mask = get_attn_pad_mask(dec_inputs, dec_inputs)
        dec_self_attn_subsequence_mask = get_attn_subsequence_mask(dec_inputs)
        dec_self_attn_mask = F.gt((dec_self_attn_pad_mask +
                                       dec_self_attn_subsequence_mask), 0)
        dec_enc_attn_mask = get_attn_pad_mask(dec_inputs, enc_inputs)
        for layer in self.layers:
            dec_outputs = layer(dec_outputs, enc_outputs, dec_self_attn_mask, dec_enc_attn_mask)
        return dec_outputs # dec_outputs: [batch_size, tgt_len, d_model]


'''
CLASStorch.nn.Transformer(d_model=512, nhead=8, num_encoder_layers=6, num_decoder_layers=6, 
                            dim_feedforward=2048, dropout=0.1, activation=<function relu>, custom_encoder=None, custom_decoder=None, 
                            layer_norm_eps=1e-05, batch_first=False, norm_first=False, bias=True, device=None, dtype=None)
'''
class Transformer(nn.Module):
    def __init__(self, d_model=512, nhead=8, num_encoder_layers=6, num_decoder_layers=6, dim_feedforward=2048, 
                src_vocab_size=6, tgt_vocab_size=9, dropout=0.1, activation=nn.ReLU, layer_norm_eps=1e-05, bias=True, dtype=None):
        super(Transformer, self).__init__()
        self.d_model = d_model
        self.nhead = nhead
        self.num_encoder_layers = num_encoder_layers
        self.num_decoder_layers = num_decoder_layers
        self.dim_feedforward = dim_feedforward
        self.dropout = dropout
        self.activation = activation
        self.layer_norm_eps = layer_norm_eps
        self.bias = bias
        self.dtype = dtype

        self.encoder = Encoder(d_model, nhead, num_encoder_layers, dim_feedforward, 
                               src_vocab_size, dropout, activation, layer_norm_eps, bias)
        self.decoder = Decoder(d_model, nhead, num_decoder_layers, dim_feedforward, 
                               tgt_vocab_size, dropout, activation, layer_norm_eps, bias)
        self.projection = nn.Linear(d_model, tgt_vocab_size)


    def forward(self, enc_inputs, dec_inputs):
        enc_outputs = self.encoder(enc_inputs)
        dec_outputs = self.decoder(dec_inputs, enc_inputs, enc_outputs) # dec_outputs: [batch_size, tgt_len, d_model]
        dec_logits = self.projection(dec_outputs) # dec_logits: [batch_size, tgt_len, tgt_vocab_size]
        return dec_logits.reshape((-1, dec_logits.shape[-1]))  #  [batch_size * tgt_len, tgt_vocab_size]
