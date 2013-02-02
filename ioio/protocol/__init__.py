#!/usr/bin/env python


from . import utils
from . import version1


def find(interface):
    """
    Find the correct protocol for this interface
    """
    p = utils.read_packet(interface, version1.response_chars)
    assert p['name'] == 'establish_connection'
    # TODO check firmware/protocol version here
    return version1.Version1Protocol(p)

__all__ = ['find']
