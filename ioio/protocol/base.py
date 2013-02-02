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

    def connect(self):
        raise NotImplementedError("Overload Protocol.connect")

    def disconnect(self):
        raise NotImplementedError("Overload Protocol.disconnect")

    def read(self, nbytes):
        raise NotImplementedError("Overload Protocol.read")

    def write(self, data):
        raise NotImplementedError("Overload Protocol.write")

    def read_packet(self):
        """
        Read a response
        """
        rtype = self.read(1)
        if (rtype not in self._response_chars):
            raise ValueError("Unknown response type: %r" % rtype)
        resp = self._response_chars[rtype]
        result = {'name': resp['name']}
        if len(resp['args']):
            data = self.read(resp['nbytes'])
            bytei = 0
            biti = 0
            for arg in resp['args']:
                if isinstance(arg[1], str):
                    nb = result[arg[1]]
                else:
                    nb = arg[1]
                if arg[0] != '':
                    result[arg[0]] = utils.extract(arg[2], nb,
                            data, bytei, biti)
                biti += nb
                if biti > 7:
                    bytei += int(biti // 8)
                    biti = biti % 8
        # TODO packets with extra data
        return result

    def write_packet(self, name, **kargs):
        pass
