#!/usr/bin/env python

import logging
import time

import ioio

logging.basicConfig(level=logging.DEBUG)

port = '/dev/ttyACM0'
pin = 1
pull = 1  # up
# 0 floating
# 1 up
# 2 down

clock = 3
# 0 16 MHz
# 1 2 MHz
# 2 250 kHz
# 3 62.5 kHz
mode = 1
# 0 positive
# 1 negative
# 2 frequency
# 3 frequency 4x
# 4 frequncy 16x
double_prec = True
incap_num = 0


try:
    import qarg
    ns = qarg.get('interface[str=%s,pin[int=%i' % \
            (port, pin))
    port = ns.interface
    pin = ns.pin
except ImportError:
    print "please install qarg for argument parsing: github.com/braingram/qarg"

i = ioio.IOIO(port, timeout=0.01)

i.write('set_pin_digital_in', pin=pin, pull=pull)
i.write('set_pin_incap', pin=pin, incap_num=incap_num, enable=True)
i.write('incap_config', incap_num=incap_num, clock=clock, mode=mode,
        double_prec=double_prec)
sp = i.read()
print sp
print "waiting for pulse on %s" % pin
pp = i.read()
try:
    while True:
        pp = i.read()
        if pp == {}:
            print "waiting for pulse on %s" % pin
            time.sleep(1.)
        else:
            print pp
except KeyboardInterrupt:
    pass

i.write('set_pin_incap', pin=pin, incap_num=incap_num, enable=False)
i.write('set_pin_digital_in', pin=pin, pull=0)
i.write('soft_reset')
del i
