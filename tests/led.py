#!/usr/bin/env python

import time

import ioio

port = '/dev/ttyACM0'

i = ioio.open(port, timeout=0.1)

# turn led on
i.digital_out(0, 0, 0)
time.sleep(1)
i.digital_out(0, 1, 0)
i.soft_reset()
