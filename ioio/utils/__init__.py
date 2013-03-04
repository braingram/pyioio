#!/usr/bin/env python

from callbacks import Callback, Callbacker


def shadow(a, b, overwrite=False, skip_private=True):
    for attr in dir(a):
        if skip_private and attr[0] == '_':
            continue
        if hasattr(b, attr) and (not overwrite):
            raise AttributeError("shadowing %s with %s will overwrite %s" %
                                 (a, b, attr))
        setattr(b, attr, getattr(a, attr))


__all__ = ['shadow', 'Callback', 'Callbacker']
