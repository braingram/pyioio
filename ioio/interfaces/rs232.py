#!/usr/bin/env python

import serial

from .base import Interface


# serial.Serial is first so read/write is overridden
class RS232Interface(serial.Serial, Interface):
    def __init__(self, port, **kwargs):
        kwargs['baudrate'] = kwargs.get('baudrate', 115200)
        serial.Serial.__init__(self, port, **kwargs)
        Interface.__init__(self)

    def connect(self):
        self.open()
        Interface.connect(self)

    def disconnect(self):
        self.close()
        Interface.disconnect(self)
