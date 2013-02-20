#!/usr/bin/env python


from . import version1


def find(interface):
    """
    Find the correct protocol for this interface
    """
    protocol = version1.Version1Protocol({})
    packet = protocol.read(interface)
    if packet['name'] != 'establish_connection':
        raise ValueError("Invalid establish_connection packet: %s" % packet)
    # TODO check firmware/protocol version here
    protocol.connection_packet = packet
    return protocol

__all__ = ['find']
