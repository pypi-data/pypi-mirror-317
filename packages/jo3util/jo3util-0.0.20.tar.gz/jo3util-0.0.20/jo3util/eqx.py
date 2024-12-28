#! /usr/bin/env python3

import json
from typing import Callable, Optional, Tuple, Union
from pathlib import Path

import equinox as eqx
import jax

from .fn import compose
from .warning import todo


def create_hook(
    fwd_pre: Callable = lambda *arg, **kwarg: None,
    fwd_post: Callable = lambda *arg, **kwarg: None,
    bwd_pre: Callable = lambda *arg, **kwarg: None,
    bwd_post: Callable = lambda *arg, **kwarg: None,
) -> Callable:
    def _create_hook(node: eqx.Module) -> eqx.Module:
        node_call = type(node).__call__

        @eqx.filter_custom_jvp
        def fwd(hook, *args, **kwargs):
            fwd_pre(*args, **kwargs)
            out = node_call(hook, *args, **kwargs)
            fwd_post(out)
            return out

        @fwd.def_jvp
        def bwd(primals, tangents):
            bwd_pre(*primals, *tangents)
            primals_out, tangents_out = eqx.filter_jvp(
                node_call, primals, tangents
            )
            bwd_post(primals_out, tangents_out)
            return primals_out, tangents_out

        class Hook(type(node)):
            def __init__(self, node):
                self.__dict__.update(node.__dict__)

            def __call__(self, *args, **kwargs):
                return fwd(self, *args, **kwargs)

        return Hook(node)

    return _create_hook


def sow(where: Callable, model: eqx.Module) -> eqx.Module:
    """Capture intermediate activations that the argument modules output
    and return them together with the model output"""
    activ = []

    def install_sow(node: Callable):
        node_call = type(node).__call__

        if isinstance(node, eqx.Module):
            todo("make StoreActivation a generic class")

            class StoreActivation(type(node)):
                def __init__(self, node):
                    self.__dict__.update(node.__dict__)

                def __call__(self, *args, **kwargs):
                    x = node_call(self, *args, **kwargs)
                    activ.append(x)
                    return x

            return StoreActivation(node)

        else:

            def store_activation(*args, **kwargs):
                x = node(*args, **kwargs)
                activ.append(x)
                return x

            return store_activation

    model = eqx.tree_at(where, model, replace_fn=install_sow)

    model_call = type(model).__call__
    todo("make Sow a generic class, also don't have nested Sows but check whether model is already a sow.")

    class Sow(type(model)):
        def __init__(self, model):
            self.__dict__.update(model.__dict__)

        def __call__(self, *args, **kwargs):
            activ.clear()  # empty the list
            x = model_call(self, *args, **kwargs)
            if isinstance(x, list):
                return activ + x
            else:
                return activ + [x]

    return Sow(model)


def insert_after(
    where: Callable,
    model: eqx.Module,
    func: Callable
) -> eqx.Module:
    """Place a callable immediately after the argument modules"""

    class Ensemble(eqx.Module):
        children: Tuple

        def __init__(self, node):
            self.children = (node, func)

        def __call__(self, *args, **kwargs):
            x = self.children[0](*args, **kwargs)
            x = self.children[1](x)
            return x

        def __getitem__(self, items):
            return self.children[items]

    model = eqx.tree_at(where, model, replace_fn=Ensemble)
    return model


def save(path: Union[Path, str], pytree, hyperparameters={}):
    with open(path, "wb") as f:
        hyperparameters = json.dumps(
            hyperparameters,
            default=lambda h: vars(h)
        )
        f.write((hyperparameters + "\n").encode())
        eqx.tree_serialise_leaves(f, pytree)


def load(path, type_):
    with open(path, "rb") as f:
        hyperparams = json.loads(f.readline().decode())
        pytree = type_(**hyperparams)
        return eqx.tree_deserialise_leaves(f, pytree)
