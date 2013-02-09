#!/usr/bin/env python
"""
see: firmware/app_layer_v1/protocol_defs.h
"""

from . import utils


class Protocol(object):
    def __init__(self, commands, responses, default_kwargs):
        self.commands = commands
        self._command_chars = utils.to_char_lookup(commands)
        self.default_kwargs = default_kwargs
        self.respones = responses
        self._response_chars = utils.to_char_lookup(responses)

    def read_response(self, interface):
        """
        Read a response
        """
        return utils.read_response(interface, self._response_chars)

    def write_command(self, interface, name, **kwargs):
        if name in self.default_kwargs:
            kw = self.default_kwargs[name].copy()
            kw.update(kwargs)
        else:
            kw = kwargs
        return utils.write_command(interface, self.commands,
            name, **kw)
