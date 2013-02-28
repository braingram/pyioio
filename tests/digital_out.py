#!/usr/bin/env python

import ioio

port = '/dev/ttyACM0'
pin = 0
open_drain = 0

i = ioio.open(port, timeout=0.1)
i.digital_out(pin, 0, open_drain)

c = raw_input('enter new value [0 or 1] for pin %s [q to quit]' % pin)
while c.strip() != 'q':
    v = c.strip()
    if v not in ('0', '1'):
        print "Invalid value: %s" % v
    else:
        v = int(v)
        i.digital_out(pin, v)
    c = raw_input('enter new value [0 or 1] for pin %s [q to quit]' % pin)
