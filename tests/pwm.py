#!/usr/bin/env python

import ioio

port = '/dev/ttyACM0'
pin = 1
freq = 100
open_drain = 0

i = ioio.open(port, timeout=0.1)
i.pwm(pin, 0., freq)

c = raw_input('enter new value duty cycle for pin %s [q to quit]' % pin)
while c.strip() != 'q':
    try:
        v = float(c.strip())
        i.pwm(pin, v)
    except Exception as e:
        print "Invalid value %s [%s]" % (c, e)
    c = raw_input('enter new value duty cycle for pin %s [q to quit]' % pin)
i.soft_reset()
