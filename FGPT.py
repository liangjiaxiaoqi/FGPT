# @Title    : Frequency-Gated Prompting for Enhancing Transformer-based EEG Decoding
# @Journal  : IEEE Journal of Biomedical and Health Informatics
# @Time     : 2025/3/18
# @Author   : Hanzhong Tan (Hank Tan)
# @GitHub   : https://github.com/liangjiaxiaoqi


import torch
from torch import nn


class FGPT(nn.Module):
    def __init__(self, dim, max_prompts=5, dropout=0.1):
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


