#!/usr/bin/env python

import ioio

port = '/dev/ttyACM0'
pin = 1
state = 'up'

i = ioio.open(port, timeout=0.1)
i.digital_in(pin)

try:
    while True:
        print i.read_response()
except KeyboardInterrupt:
    i.soft_reset()
