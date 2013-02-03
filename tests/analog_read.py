#!/usr/bin/env python

import logging
logging.basicConfig(level=logging.DEBUG)

import ioio

port = '/dev/ttyACM0'
pin = 31
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

i = ioio.IOIO(port, timeout=0.1)

i.write('set_pin_analog_in', pin=pin)
i.write('set_analog_in_sampling', pin=pin, enable=True)

analog_format = i.read()
assert analog_format['name'] == 'report_analog_in_format'
pins = analog_format['pins']


def read_channel():
    header = ord(i.interface.read())
    high = ord(i.interface.read())
    value = (header & 0x03) | (high << 2)
    return value


def analog_read():
    packet = i.read()
    if packet['name'] == 'report_analog_in_status':
        values = {}
        for pi in pins:
            values[pi] = read_channel()
        packet['values'] = values
    return packet

try:
    while True:
        print analog_read()
except KeyboardInterrupt:
    i.write('soft_reset')
