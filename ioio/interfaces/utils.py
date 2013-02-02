#!/usr/bin/env python


def find(port, **kwargs):
    # only rs232 for now
    return rs232.RS232Interface(port, **kwargs)
