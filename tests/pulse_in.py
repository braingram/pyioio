#!/usr/bin/env python

import ioio

port = '/dev/ttyACM0'
pin = 1
pull = 'up'
clock = '250kHz'
mode = 'positive'
double = False

i = ioio.open(port, timeout=0.1)
i.pulse_in(pin, clock=clock, mode=mode, pull=pull, double=double)

try:
    while True:
        print i.read_response()
except KeyboardInterrupt:
    i.soft_reset()
