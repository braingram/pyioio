#!/usr/bin/env python

import serial

from .base import Interface


class RS232Interface(Interface, serial.Serial):
    def __init__(self, port, **kwargs):
        if ('baudrate' not in kwargs):
            kwargs['baudrate'] = 115200
        Serial.__init__(self, port, **kwargs)
        Interface.__init__(self)

    def connect(self):
        self.open()
        Interface.connect(self)

    def disconnect(self):
        self.close()
        Interface.disconnect(self)
