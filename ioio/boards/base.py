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
    def __init__(self, protocol, pins, n_pwm, n_uarts, n_spi, incap_doubles,
            incap_singles, twi_pins, icsp_pins):
        self.pins = pins
        self.n_uarts = n_uarts
        self.n_spi = n_spi
        self.incap_doubles = incap_doubles
        self.incap_singles = incap_singles
        self.twi_pins = twi_pins
        self.icsp_pins = icsp_pins
        pass

    def get_n_pins(self):
        return len(self.pins)
    n_pins = property(get_n_pins)

    def get_n_analog_pins(self):
        return reduce(lambda x, y: x + int(y.analog), self.pins, 0)
    n_analog_pins = property(get_n_analog_pins)

    def valid_pin(self, i):
        return ((i >= 0) and (i < len(self.pins)))

    def valid_p_in(self, i):
        return (self.valid_pin(i) and self.pins[i].p_in)

    def valid_p_out(self, i):
        return (self.valid_pin(i) and self.pins[i].p_out)

    def valid_analog(self, i):
        return (self.valid_pin(i) and self.pins[i].analog)
