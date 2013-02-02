#!/usr/bin/env python
"""
see: firmware/app_layer_v1/protocol_defs.h
"""

from . import utils


class Protocol(object):
    def __init__(self, commands, responses):
        self.commands = commands
        self._command_chars = utils.to_char_lookup(commands)
        self.respones = responses
        self._response_chars = utils.to_char_lookup(responses)

    def read_packet(self, interface):
        """
        Read a response
        """
        return utils.read_packet(interface, self._response_chars)

    def write_packet(self, interface, name, **kargs):
        return utils.write_packet(interface, self.commands,
            name, **kwargs)
