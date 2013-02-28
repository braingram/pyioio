#!/usr/bin/env python

import ioio

port = '/dev/ttyACM0'
pin = 31

i = ioio.open(port, timeout=0.1)
i.analog_in(pin)

try:
    while True:
        print i.read_response()
except KeyboardInterrupt:
    i.soft_reset()
