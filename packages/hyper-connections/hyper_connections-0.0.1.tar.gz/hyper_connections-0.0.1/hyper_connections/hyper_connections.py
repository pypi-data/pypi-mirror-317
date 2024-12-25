from __future__ import annotations
from functools import partial
from random import randrange

import torch
from torch import nn
from torch.nn import Module
import torch.nn.functional as F

from einops import rearrange, repeat, reduce, einsum

# helper functions

def exists(v):
    return v is not None

def default(v, d):
    return v if exists(v) else d

# main class

# hyper connection residual streams

class HyperConnections(Module):
    def __init__(
        self,
        num_residual_streams,
        *,
        dim,
        branch: Module | None = None,
        layer_index = None,
        tanh = True,
    ):
        """
        Appendix J, Algorithm2 in - https://arxiv.org/abs/2409.19606
        """
        super().__init__()

        self.branch = branch

        self.act = nn.Tanh() if tanh else nn.Identity()
        self.norm = nn.RMSNorm(dim)

        self.num_residual_streams = num_residual_streams
        init_residual_index = default(layer_index, randrange(num_residual_streams)) % num_residual_streams # just choose one random residual stream if layer index not given

        self.static_beta = nn.Parameter(torch.ones(num_residual_streams))

        init_alpha0 = torch.zeros((num_residual_streams, 1))
        init_alpha0[init_residual_index, 0] = 1.

        self.static_alpha = nn.Parameter(torch.cat([init_alpha0, torch.eye(num_residual_streams)], dim = 1))

        self.dynamic_alpha_fn = nn.Parameter(torch.zeros(dim, num_residual_streams + 1))
        self.dynamic_alpha_scale = nn.Parameter(torch.ones(()) * 1e-2)
        self.dynamic_beta_fn = nn.Parameter(torch.zeros(dim))
        self.dynamic_beta_scale = nn.Parameter(torch.ones(()) * 1e-2)

    @classmethod
    def get_expand_reduce_stream_functions(cls, num_streams):
        expand_fn = partial(repeat, pattern = 'b ... -> (b s) ...', s = num_streams)
        reduce_fn = partial(reduce, pattern = '(b s) ... -> b ...', reduction = 'sum', s = num_streams)

        return expand_fn, reduce_fn

    def width_connection(self, residuals):
        # width connection

        residuals = rearrange(residuals, '(b s) ... d -> b ... s d', s = self.num_residual_streams)

        normed = self.norm(residuals)

        wc_weight = self.act(normed @ self.dynamic_alpha_fn)
        dynamic_alpha = wc_weight * self.dynamic_alpha_scale
        alpha = dynamic_alpha + self.static_alpha

        dc_weight = self.act(normed @ self.dynamic_beta_fn)
        dynamic_beta = dc_weight * self.dynamic_beta_scale
        beta = dynamic_beta + self.static_beta

        # width connection

        mix_h = einsum(alpha, residuals, '... s t, ... s d -> ... t d')

        branch_input, residuals = mix_h[..., 0, :], mix_h[..., 1:, :]

        return branch_input, residuals, beta

    def depth_connection(self, branch_output, residuals, beta):
        # 'depth' connection

        residuals = einsum(branch_output, beta, 'b ... d, b ... s -> b ... s d') + residuals
        return rearrange(residuals, 'b ... s d -> (b s) ... d')

    def forward(self, residuals, **branch_kwargs):

        branch_input, residuals, beta = self.width_connection(residuals)

        def add_residual_fn(branch_out):
            return self.depth_connection(branch_out, residuals, beta)

        if not exists(self.branch):
            return branch_input, add_residual_fn

        branch_output = self.branch(branch_input, **branch_kwargs)

        return add_residual_fn(branch_output)
