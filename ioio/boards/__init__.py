#!/usr/bin/env python

from . import otg


def find(protocol):
    if not hasattr(protocol, 'connection_packet'):
        raise ValueError('Invalid protocol, missing connection_packet: %s' \
            % protocol)
    p = protocol.connection_packet
    # TODO add other boards
    return otg.OTG(protocol)
