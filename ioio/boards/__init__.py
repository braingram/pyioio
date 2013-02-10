#!/usr/bin/env python

from . import versions


def find(protocol):
    if not hasattr(protocol, 'connection_packet'):
        raise ValueError('Invalid protocol, missing connection_packet: %s' \
            % protocol)
    p = protocol.connection_packet
    v = p['hardware_version']
    if v == 'SPRK0020':
        return versions.SPRK0020(protocol)
    elif v == 'SPRK0016':
        return versions.SPRK0016(protocol)
    elif v == 'SPRK0015':
        return versions.SPRK0015(protocol)
    elif v == 'MINT0010':
        return versions.SPRK0010(protocol)
    else:
        raise ValueError('Unknown hardware version: %s' % v)
