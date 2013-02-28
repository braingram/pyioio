#!/usr/bin/env python

import ioio

port = '/dev/ttyACM0'
pin = 31

try:
    import qarg
    ns = qarg.get('interface[str=%s,pin[int=%i' %
                  (port, pin))
    port = ns.interface
    pin = ns.pin
except ImportError:
    print "please install qarg for argument parsing: github.com/braingram/qarg"

i = ioio.open(port, timeout=0.1)
i.analog_in(pin)

try:
    while True:
        print i.read_response()
except KeyboardInterrupt:
    i.soft_reset()
