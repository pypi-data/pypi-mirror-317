from __future__ import annotations
from typing import Callable

from functools import partial
from random import randrange

import torch
from torch import nn
from torch.nn import Module
import torch.nn.functional as F
from torch.utils._pytree import tree_flatten, tree_unflatten

from einops import rearrange, repeat, reduce, einsum

from hyper_connections.hyper_connections import Residual, StreamEmbed

# helper functions

def exists(v):
    return v is not None

def default(v, d):
    return v if exists(v) else d

def identity(t):
    return t

# main classes

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
        channel_first = False,
        num_branch_inputs = 1  # residuals will be linearly combined to multiple inputs, fed through the branch, then linearly combined back out to residuals
    ):
        """
        Appendix J, Algorithm2 in - https://arxiv.org/abs/2409.19606
        """
        super().__init__()

        self.branch = branch

        # activation, seemingly results were wishy washy depending on using tanh or not

        self.act = nn.Tanh() if tanh else nn.Identity()

        self.norm = nn.RMSNorm(dim) # they used layernorm in paper, but rmsnorm is fine given what we know now

        self.num_residual_streams = num_residual_streams
        self.num_branch_inputs = num_branch_inputs

        init_residual_index = default(layer_index, randrange(num_residual_streams)) % num_residual_streams # just choose one random residual stream if layer index not given

        self.static_beta = nn.Parameter(torch.ones(num_residual_streams, num_branch_inputs))

        init_alpha0 = torch.zeros((num_residual_streams, num_branch_inputs))
        init_alpha0[init_residual_index, :] = 1.

        self.static_alpha = nn.Parameter(torch.cat([init_alpha0, torch.eye(num_residual_streams)], dim = 1))

        self.dynamic_alpha_fn = nn.Parameter(torch.zeros(dim, num_residual_streams + num_branch_inputs))
        self.dynamic_alpha_scale = nn.Parameter(torch.ones(()) * 1e-2)
        self.dynamic_beta_fn = nn.Parameter(torch.zeros(dim, num_branch_inputs))
        self.dynamic_beta_scale = nn.Parameter(torch.ones(()) * 1e-2)

        # channel first option

        self.channel_first = channel_first

    @classmethod
    def get_expand_reduce_stream_functions(cls, num_streams):
        if disable:
            return (identity, identity)

        expand_fn = partial(repeat, pattern = 'b ... -> (b s) ...', s = num_streams)
        reduce_fn = partial(reduce, pattern = '(b s) ... -> b ...', reduction = 'sum', s = num_streams)

        return expand_fn, reduce_fn

    @classmethod
    def get_init_and_expand_reduce_stream_functions(cls, num_streams, disable = False):

        hyper_conn_klass = cls if not disable else Residual

        init_hyper_conn_fn = partial(hyper_conn_klass, num_streams)
        expand_reduce_fns = cls.get_expand_reduce_stream_functions(num_streams, disable = disable)

        return (init_hyper_conn_fn, *expand_reduce_fns)

    def width_connection(self, residuals):
        num_streams, num_branch_inputs = self.num_residual_streams, self.num_branch_inputs

        # width connection

        if self.channel_first:
            residuals = rearrange(residuals, 'b d ... -> b ... d')

        residuals = rearrange(residuals, '(b s) ... d -> b ... s d', s = num_streams)

        normed = self.norm(residuals)

        # alpha for weighted sum of residuals going into branch

        wc_weight = self.act(normed @ self.dynamic_alpha_fn)
        dynamic_alpha = wc_weight * self.dynamic_alpha_scale
        alpha = dynamic_alpha + self.static_alpha

        # beta for weights from branch output back to residual streams

        dc_weight = self.act(normed @ self.dynamic_beta_fn)
        dynamic_beta = dc_weight * self.dynamic_beta_scale

        beta = dynamic_beta + self.static_beta

        mix_h = einsum(alpha, residuals, '... s t, ... s d -> ... t d')

        branch_input, residuals = mix_h[..., :-num_streams, :], mix_h[..., -num_streams:, :]

        branch_input = rearrange(branch_input, 'b ... i d -> (i b) ... d')

        if self.channel_first:
            branch_input = rearrange(branch_input, 'b ... d -> b d ...')

        return branch_input, residuals, dict(beta = beta)

    def depth_connection(self, branch_output, residuals, *, beta):
        # 'depth' connection

        if self.channel_first:
            branch_output = rearrange(branch_output, 'b d ... -> b ... d')

        branch_output = rearrange(branch_output, '(i b) ... -> i b ...', i = self.num_branch_inputs)

        residuals = einsum(branch_output, beta, 'i b ... d, b ... s i -> b ... s d') + residuals

        output = rearrange(residuals, 'b ... s d -> (b s) ... d')

        if self.channel_first:
            output = rearrange(output, 'b ... d -> b d ...')

        return output

    def decorate_branch(self, branch: Callable):
        assert not exists(self.branch), 'branch was already wrapped on init'

        def forward_and_add_residual(residual, *args, **kwargs):
            branch_input, add_residual = self.forward(residual)

            branch_output = branch(branch_input, *args, **kwargs)

            residual = add_residual(branch_output)

            return residual

        return forward_and_add_residual

    def forward(self, residuals, *branch_args, **branch_kwargs):

        branch_input, residuals, residual_kwargs = self.width_connection(residuals)

        def add_residual_fn(branch_out):
            (branch_out, *rest), tree_spec = tree_flatten(branch_out)

            branch_out = self.depth_connection(branch_out, residuals, **residual_kwargs)

            return tree_unflatten((branch_out, *rest), tree_spec)

        if not exists(self.branch):
            return branch_input, add_residual_fn

        branch_output = self.branch(branch_input, *branch_args, **branch_kwargs)

        return add_residual_fn(branch_output)
