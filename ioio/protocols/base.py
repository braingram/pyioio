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

    def read_response(self, interface):
        """
        Read a response
        """
        return utils.read_response(interface, self._response_chars)

    def write_command(self, interface, name, **kwargs):
        return utils.write_command(interface, self.commands,
            name, **kwargs)
