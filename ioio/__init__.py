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
    """
    Main IOIO class

    Contains
        interface : communication interface
        protocol : packet spec
        board : hardware/pin spec
    """
    def __init__(self, port, **kwargs):
        """
        Construct a connection
        """
        self.port = port
        self.interface = interfaces.find(port, **kwargs)
        self.protocol = protocols.find(self.interface)
        self.board = boards.find(self.protocol)

    def read(self):
        self.protocol.read_response(self.interface)

    def write(self, name, **kwargs):
        self.protocol.write_command(self.interface, name, **kwargs)


__all__ = ['IOIO']
