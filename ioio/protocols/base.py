#!/usr/bin/env python
"""
see: firmware/app_layer_v1/protocol_defs.h
"""


class Protocol(object):
    def __init__(self, commands, responses, default_kwargs):
        self.commands = commands
        self.responses = responses

    def read(self, interface):
        return self.responses.read(interface)

    def write(self, interface, name, *args):
        self.command.write(interface, name, *args)
