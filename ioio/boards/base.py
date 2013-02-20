#!/usr/bin/env python

import collections


Pin = collections.namedtuple('Pin', ('p_in', 'p_out', 'analog'))


def make_pin_list(p_in, p_out, analog, n=None):
    if n is None:
        n = max(max(p_in), max(p_out), max(analog))
    pins = []
    for i in xrange(n):
        pins.append(Pin(i in p_in, i in p_out, i in analog))
    return pins


class Board(object):
    def __init__(self, protocol, pins, n_pwms, n_uarts, n_spis, incap_doubles,
            incap_singles, twi_pins, icsp_pins):
        self.pins = {
            'p_in': hwmodules.PinSet(pins['p_in']),
            'p_out': hwmodules.PinSet(pins['p_out']),
            'analog': hwmodules.PinSet(pins['analog']),
            'pwm': hwmodules.PWM(n_pwms),
            'uart': hwmodules.UART(n_uarts),
            'spi': hwmodules.SPI(n_spis),
            'incap_double': hwmodules.IncapDouble(incap_doubles),
            'incap_single': hwmodules.IncapSingle(incap_singles),
            'twi': hwmodules.TWI(twi_pins),
            'icsp': hwmodules.ICSP(icsp_pins),
        }

    def valid_pin(self, i, module):
        return self.pins[module].valid_pin(i)

    def pin(self, i, module, value=None):
        return self.pins[module].pin(i, value)

    def valid_module(self, i, module):
        return self.pins[module].valid(i)

    def item(self, i, module, value=None):
        return self.pins[module].item(i, value)

    def available_pin(self, module, exclude=None):
        return self.pins[module].available_pin(exclude)

    def available_module(self, module, exclude=None):
        return self.pins[module].available(exclude)
