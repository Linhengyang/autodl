import torch
from torch import nn
from ..Base.SubModules.AddLNorm import AddLNorm
from ..Base.RootLayers.AttentionPools import MultiHeadAttention

class PositionWiseFFN(nn.Module):
    '''
    args: ffn_num_hiddens, ffn_num_outputs
        ffn_num_hiddens: the hidden size inside the MLP
        ffn_num_outputs: output size of the MLP, usually the same as the input size
    
    inputs: X

    returns: denoted as O
    
    explains:
        Perform the same MLP on every position. So only one MLP is enough.
    '''
    def __init__(self, ffn_num_hiddens, ffn_num_outputs):
        super().__init__()
        self.dense1 = nn.LazyLinear(ffn_num_hiddens)
        self.relu = nn.ReLU()
        self.dense2 = nn.LazyLinear(ffn_num_outputs)
    
    def forward(self, X):
        return self.dense2(self.relu(self.dense1(X)))

class TransformerEncoderBlock(nn.Module):
    '''
    components: 
        1. multihead attention(self-att) 
        2. addLnorm 
        3. positionwiseFFN 
        4. addLnorm 
    args:
        num_heads, num_hiddens, dropout, ffn_num_hiddens, use_bias=False

    inputs: enc_X, valid_lens(optional) 
        enc_X's shape: (batch_size, seq_len, d_dim) 
        valid_lens(optional)'s shape: (batch_size,) since it's self-att here 
    
    returns: denoted as enc_O 
        enc_O's shape: (batch_size, seq_len, d_dim), the same as enc_X 
    
    explains: 
        keep batch shape at every layer's input/output through the block 
        encode source sequence time 1 to T directly to deep sequence time 1 to T, that is: 
            f(time 1 to T) --> node 1 to T on next layer 
    '''
    def __init__(self, num_heads, num_hiddens, dropout, ffn_num_hiddens, use_bias=False):
        super().__init__()
        self.attention = MultiHeadAttention(num_heads, num_hiddens, dropout, use_bias)
        self.addlnorm1 = AddLNorm(num_hiddens, dropout)
        self.PosFFN = PositionWiseFFN(ffn_num_hiddens, num_hiddens)
        self.addlnorm2 = AddLNorm(num_hiddens, dropout)
    
    def forward(self, X, valid_lens):
        Y = self.addlnorm1(X, self.attention(X, X, X, valid_lens))
        return self.addlnorm2(Y, self.PosFFN(Y))

class TransformerDecoderBlock(nn.Module):
    '''
    components:
        1. masked multihead attention(self-att but using a mask to be auto-regressive)
        2. addLnorm
        3. encoder-decoder attention(use sequences from decoder as queries, keys&values are from encoder)
        4. addLnorm
        5. positionwiseFFN
        6. addLnorm

    args:
        blk_ind, num_heads, num_hiddens, dropout, ffn_num_hiddens, use_bias=False
        
    inputs: dec_X, state
        dec_X's shape: (batch_size, seq_len, d_dim)
        state:
            self-att???, ???????????????????????????, ??????infer???????????????
            enc-dec-att???, ?????????????????????encoder output????????????, ???decoder????????????source sequence???????????????
    
    returns: denoted as dec_O
        dec_O's shape: (batch_size, seq_len, d_dim), the same as dec_X
    
    explains:
        keep batch shape at every layer's input/output through the block
    '''
    def __init__(self, blk_ind, num_heads, num_hiddens, dropout, ffn_num_hiddens, use_bias=False):
        super().__init__()
        self.blk_ind = str(blk_ind)
        self.attention1 = MultiHeadAttention(num_heads, num_hiddens, dropout, use_bias)
        self.addlnorm1 = AddLNorm(num_hiddens, dropout)
        self.attention2 = MultiHeadAttention(num_heads, num_hiddens, dropout, use_bias)
        self.addlnorm2 = AddLNorm(num_hiddens, dropout)
        self.PosFFN = PositionWiseFFN(ffn_num_hiddens, num_hiddens)
        self.addlnorm3 = AddLNorm(num_hiddens, dropout)
    
    def forward(self, X, enc_info, infer_recorder=None): # ???????????????infer_recorder???in-place??????
        src_enc_seqs, src_valid_lens = enc_info
        # X' shape, train: (batch_size, seq_len, d_dim), infer: (1, 1, d_dim)
        # src_enc_seqs'shape, train: (batch_size, seq_len, d_dim), infer: (1, seq_len, d_dim)
        # src_valid_lens's shape, train: (batch_size,), infer: (1,)
        if self.training: # train?????????
            assert X.shape[-1] == src_enc_seqs.shape[-1], f'training: enc output & dec input block {self.blk_ind} are not in same shape'
            assert X.shape[0] == src_enc_seqs.shape[0] == src_valid_lens.shape[0], f'enc output & enc valid lens & dec input block {self.blk_ind} differ batch_size'
            batch_size, seq_len = X.shape[:-1]
            mask = torch.arange(1, seq_len+1, dtype=torch.int32, device=X.device).repeat(batch_size, 1)
            KVs, infer_recorder = X, None # ????????????, ????????????mask??????auto-regressive, train??????????????????infer_recorder
        else: # infer?????????
            # infer_recoder?????????dict of (1, _, d_dim) tensor
            assert type(infer_recorder) == dict, 'in infer mode, a dictionary as infer recorder should be input'
            try: 
                infer_recorder[self.blk_ind] = torch.cat([infer_recorder[self.blk_ind], X], dim=1)
            except KeyError: # ???<bos> infer?????????token???, infer_recorder?????????????????????
                infer_recorder[self.blk_ind] = X
            KVs, mask = infer_recorder[self.blk_ind], None # ?????????recorded tokens???????????????K???V, infer??????????????????mask
        Y = self.addlnorm1(X, self.attention1(X, KVs, KVs, mask))
        Z = self.addlnorm2(Y, self.attention2(Y, src_enc_seqs, src_enc_seqs, src_valid_lens))
        return self.addlnorm3(Z, self.PosFFN(Z)), infer_recorder
