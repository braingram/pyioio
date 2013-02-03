#!/usr/bin/env python

import logging
logging.basicConfig(level=logging.DEBUG)
import sys

import ioio


p = '/dev/ttyACM0'
if len(sys.argv) > 1:
    p = sys.argv[1]

i = ioio.IOIO(p)

i.write('set_pin_digital_out', pin=0, open_drain=1, value=1)

_ = raw_input('Press enter to turn on led')
i.write('set_digital_out_level', pin=0, value=0)

_ = raw_input('Press enter to turn off led')
i.write('set_digital_out_level', pin=0, value=1)

_ = raw_input('Press enter to exit...')
i.write('soft_reset')
