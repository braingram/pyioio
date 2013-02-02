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


class IOIO(object):
     def __init__(self, port, **kwargs):
        self.port = port
        self.interface = interfaces.find(port, **kwargs)
        self.protocol = protocols.find(self.interface)
        self.board = boards.find(self.protocol)


__all__ = ['IOIO']
