#!/usr/bin/env python

import logging
import select
import sys
import time

import ioio

logging.basicConfig(level=logging.DEBUG)

port = '/dev/ttyACM0'
rx_pin = 6
tx_pin = 7
uart_num = 0
#direction = 0
# 0 tx
# 1 rx
speed4x = False
rate = 9600
parity = 0
# 0 none
# 1 even
# 2 odd
two_stop_bits = False

i = ioio.IOIO(port, timeout=0.01)

i.write('set_pin_uart', pin=rx_pin, uart_num=uart_num, dir=1, enable=True)
i.write('set_pin_uart', pin=tx_pin, uart_num=uart_num, dir=0, enable=True)
i.write('uart_config', uart_num=uart_num, rate=rate, speed4x=speed4x,
        two_stop_bits=two_stop_bits, parity=parity)


def read_input():
    rlist, _, _ = select.select([sys.stdin], [], [], 1)
    if rlist:
        return sys.stdin.readline().strip()
    else:
        return None

try:
    while True:
        data = read_input()  # has timeout
        if data is not None:
            i.write('uart_data', uart_num=uart_num, data=data,
                    size=len(data) * 8)
        p = i.read()
        if p != {}:
            print p
except KeyboardInterrupt:
    pass

i.write('set_pin_digital_in', pin=rx_pin, pull=0)
i.write('set_pin_digital_in', pin=tx_pin, pull=0)
i.write('soft_reset')
del i
