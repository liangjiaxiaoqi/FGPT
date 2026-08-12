# Frequency-Gated Prompting for Enhancing Transformer-based EEG Decoding
# @Time   : 2025/3/18
# @Author : Hanzhong Tan (Hank Tan)
# @GitHub : https://github.com/liangjiaxiaoqi

import torch
from torch import nn


class FGPT(nn.Module):
    def __init__(self, dim, max_prompts=10, dropout=0.1):
        super().__init__()
        self.max_prompts = max_prompts

        # 可学习的提示嵌入和门控参数
        self.prompt_embeddings = nn.Parameter(torch.randn(1, max_prompts, dim))
        self.prompt_gate = nn.Parameter(torch.ones(max_prompts))  # 初始全开

        self.prompt_dropout = nn.Dropout(dropout)
        self.prompt_proj = nn.Linear(dim, dim)

    def forward(self, x):
        # 计算门控权重并保持梯度流
        gates = torch.sigmoid(self.prompt_gate)  # (max_prompts,)

        # 投影提示嵌入并应用门控
        projected = self.prompt_proj(self.prompt_embeddings)  # (1, max_prompts, dim)
        gated_prompts = projected * gates.view(1, -1, 1)  # 门控加权
        # gated_prompts = projected

        # 扩展并应用FFT
        batch_prompts = gated_prompts.expand(x.size(0), -1, -1)
        fft_prompts = torch.fft.fft(self.prompt_dropout(batch_prompts), dim=-1).real
        # fft_prompts = batch_prompts

        # 拼接处理后的提示与原始特征,并返回FFT提示token数量
        return torch.cat((fft_prompts, x), dim=1), fft_prompts.size(1)

class Attention(nn.Module):
    def __init__(self, dim, heads = 8, dim_head = 64, dropout = 0.):
        super().__init__()
        inner_dim = dim_head *  heads
        project_out = not (heads == 1 and dim_head == dim)

        self.heads = heads
        self.scale = dim_head ** -0.5

        self.attend = nn.Softmax(dim = -1)
        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias = False)

        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, dim),
            nn.Dropout(dropout)
        ) if project_out else nn.Identity()

        # add code of fft prompts
        # self.prompt_embeddings = nn.Parameter(torch.randn(1, 5, dim))  # num_prompts
        # self.prompt_dropout = nn.Dropout(dropout)
        # self.prompt_proj = nn.Linear(dim, dim)

        self.fft = FGPT(dim=dim, max_prompts=3, dropout=dropout) # FATIG:3;23都试过了不好,1略好,4比1略好,5不好,6比1略好 dropout
        # add code of fft prompts

    def forward(self, x):
        # add code of fft prompts
        # x = torch.cat((#x[:, :1, :],
        #                torch.fft.fft(torch.fft.fft(self.prompt_dropout(self.prompt_proj(self.prompt_embeddings).expand(x.shape[0], -1, -1)), dim=-1), dim=-2).real,
        #                x[:, 0:, :]), dim=1
        #               )
        x, num_prompts = self.fft(x)
        # add code of fft prompts

        qkv = self.to_qkv(x).chunk(3, dim = -1)
        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h = self.heads), qkv)

        dots = torch.matmul(q, k.transpose(-1, -2)) * self.scale

        attn = self.attend(dots)

        out = torch.matmul(attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')

        out = out[:, num_prompts:, :]  # self.num_prompts-2
        return self.to_out(out)


