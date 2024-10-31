import torch 
import torch.nn as nn
import math

class InputEmbeddings(nn.Module):
    
    def __init__(self, d_model: int, vocab_size: int):
        """ d_model = size of the embedding vector.
            vocab_size = self explanatory    """
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, d_model)

    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)
    

    
class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int , seq_len:int, dropout: float) ->None:
        """ seq_length = maximum length of the sentence. """

        self.d_model = d_model
        self.seq_len = seq_len
        self.dropout = nn.Dropout(dropout)

        # create a matrix of shape (seq_len , d_model)
        pe = torch.zeros(seq_len,d_model)
        #create a vector of shape(Seq_len, 1)
        position = torch.arange(0, seq_len, dtype = torch.float).unsqueeze(1) 
        div_term = torch.exp(torch.arange(0,d_model,2).float() * (-math.log(10000.0)/d_model))

        # apply the sine and cosine to even and odd positions respecrtively

        pe[:,0::2] = torch.sin(position * div_term)
        pe[:,1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)     #(1,Seq_Len, d_model)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        x = x + (self.pe[:, :x.shape[1], :]).requires_grad(False)
        return self.dropout(x)

