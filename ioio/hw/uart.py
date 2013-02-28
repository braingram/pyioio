#!/usr/bin/env python

from base import HWWithSubmodules


class UARTSubModule(object):
    def __init__(self):
        self.baud = 9600
        self.parity = 0
        self.two_stop_bits = 0
        self.speed4x = 0

    def check_config(self, config):
        """
        Returns True when config needs updating
        """
        for k in config:
            if not hasattr(self, k):
                raise ValueError("Inalid config key [%s]" % k)
            if config[k] != getattr(self, k):
                return False
        return True

    def set_config(self, config):
        for k in config:
            if not hasattr(self, k):
                raise ValueError("Inalid config key [%s]" % k)
            setattr(self, k, config[k])
    
    def get_config(self):
        return dict([(k, getattr(self, k)) for k in
                     ('baud', 'parity', 'two_stop_bits', 'speed4x')])


class UART(HWWithSubmodules):
    def __init__(self, pins, subs=None):
        HWWithSubmodules.__init__(self, pins, subs, UARTSubModule)
