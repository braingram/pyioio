#!/usr/bin/env python

from . import rs232


def find(port, **kwargs):
    # only rs232 for now
    return rs232.RS232Interface(port, **kwargs)

__all__ = ['find']
