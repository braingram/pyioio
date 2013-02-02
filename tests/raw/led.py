#!/usr/bin/env python

import serial
import sys

p = '/dev/ttyACM0'

if len(sys.argv) > 1:
    p = sys.argv[1]

s = serial.Serial(p, 115200)

ptype = s.read(1)  # packet type
magic = s.read(4)  # IOIO
hwv = s.read(8)
brv = s.read(8)
fwv = s.read(8)

print("PType   : '%s'" % ptype)
print("Magic   : '%s'" % magic)
print("Hardware: '%s'" % hwv)
print("Board   : '%s'" % brv)
print("Firmware: '%s'" % fwv)

# sets digital pin 0 to output
s.write('\x03')  # set digital pin
s.write('\x01')  # open drain
s.write('\x00')  # pin

i = raw_input('Press enter to close...')

s.write('\x01')  # soft reset
s.close()
