#!/usr/bin/env python
"""
see: firmware/app_layer_v1/protocol_defs.h
"""

from .. import utils


class Protocol(object):
    def __init__(self, interface, commands, responses):
        self.commands = commands
        self.responses = responses
        self.interface = interface
        # shadow interface functions
        utils.shadow(interface, self)

    def read_response(self):
        return self.responses.read(self.interface)

    def write_command(self, *args, **kwargs):
        return self.commands.write(self.interface, *args, **kwargs)
