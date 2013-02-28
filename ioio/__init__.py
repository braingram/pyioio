#!/usr/bin/env python
"""
Each IOIO contains:
    - protocol : protocol version (packet spec)
    - board : physical hardware (pin spec)
    - interface : communication interface
"""

from . import boards
from . import interfaces
from . import protocols

pyopen = open


def open(port, **kwargs):
    interface = interfaces.find(port, **kwargs)
    protocol = protocols.find(interface)
    return boards.find(protocol)


__all__ = []
