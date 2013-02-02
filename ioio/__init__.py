#!/usr/bin/env python
"""
Each IOIO contains:
    - protocol : protocol version (packet spec)
    - board : physical hardware (pin spec)
    - interface : communication interface
"""

from . import board, interface, protocol


class IOIO(object):
     def __init__(self, port, **kwargs):
        self.port = port
        self.interface = interface.find(port, **kwargs)
        self.protocol = protocol.find(interface)
        self.board = board.find(protocol)
