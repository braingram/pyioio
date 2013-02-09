#!/usr/bin/env python

import logging
logging.basicConfig(level=logging.DEBUG)

import ioio

port = '/dev/ttyACM0'
pin = 0
state = 0
# 0 = floating
# 1 = pull-up
# 2 = pull-down

try:
    import qarg
    ns = qarg.get('interface[str=%s,pin[int=%i,state[int=%i' % \
            (port, pin, state))
    port = ns.interface
    pin = ns.pin
    state = ns.state
except ImportError:
    print "please install qarg for argument parsing: github.com/braingram/qarg"

i = ioio.IOIO(port)

i.write('set_pin_digital_in', pin=pin, pull=state)
i.write('set_change_notify', pin=pin, cn=True)

# change notify
cn = i.read()  # should be a 'set_change_notify' event
print cn
assert cn['name'] == 'set_change_notify'
di = i.read()  # should be a 'report_digital_in_status' event
print di
assert di['name'] == 'report_digital_in_status'

i.write('set_change_notify', pin=pin, cn=False)
i.write('set_pin_digital_in', pin=pin, pull=0)
i.write('soft_reset')
del i
