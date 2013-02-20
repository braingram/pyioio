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
        self.pins = pins
        self.n_pwms = n_pwms
        self.n_uarts = n_uarts
        self.n_spis = n_spis
        self.incap_doubles = incap_doubles
        self.incap_singles = incap_singles
        self.twi_pins = twi_pins
        self.icsp_pins = icsp_pins

        self.used = {}
        self.used_pwms = [False] * self.n_pwms
        self.used_uarts = [False] * self.n_uarts
        self.used_spis = [False] * self.n_spis
        self.used_incap_doubles = dict([(i, False) for i in \
                self.incap_doubles])
        self.used_incap_singles = dict([(i, False) for i in \
                self.incap_singles])
        self.used_twi_pins = dict([(i[0], False) for i in \
                self.twi_pins])
        self.used_icsp = False

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

    def use_pin(self, i, function):
        self.used[i] = function

    def pin_in_use(self, i):
        return self.used.get(i, False)

    def get_pins_in_use(self, function=None):
        if function is None:
            return self.used.keys()
        return filter(lambda k: self.used[k] == function, self.used)

    def use_pwm(self, i):
        if (i >= self.n_pwms):
            raise ValueError('pwm index[%s] > n_pwms[%s]' % \
                    (i, self.n_pwms))
        self.used_pwms[i] = True

    def pwm_in_use(self, i):
        if (i >= self.n_pwms):
            raise ValueError('pwm index[%s] > n_pwms[%s]' % \
                    (i, self.n_pwms))
        return self.used_pwms[i]

    def use_uart(self, i):
        if (i >= self.n_uarts):
            raise ValueError('uart index[%s] > n_uarts[%s]' % \
                    (i, self.n_uarts))
        self.used_uarts[i] = True

    def uart_in_use(self, i):
        if (i >= self.n_uarts):
            raise ValueError('uart index[%s] > n_uarts[%s]' % \
                    (i, self.n_uarts))
        return self.used_uarts[i]

    def use_spi(self, i):
        if (i >= self.n_spis):
            raise ValueError('spi index[%s] > n_spis[%s]' % \
                    (i, self.n_spis))
        self.used_spis[i] = True

    def spi_in_use(self, i):
        if (i >= self.n_spis):
            raise ValueError('spi index[%s] > n_spis[%s]' % \
                    (i, self.n_spis))
        return self.used_spis[i]

    def use_incap_double(self, i):
        if i not in self.incap_doubles:
            raise ValueError('invalid incap_double index[%s] not in %s' % \
                    (i, self.incap_doubles))
        self.used_incap_doubles[i] = True

    def incap_double_in_use(self, i):
        if i not in self.incap_doubles:
            raise ValueError('invalid incap_double index[%s] not in %s' % \
                    (i, self.incap_doubles))
        return self.used_incap_doubles[i]

    def use_incap_single(self, i):
        if i not in self.incap_singles:
            raise ValueError('invalid incap_single index[%s] not in %s' % \
                    (i, self.incap_singles))
        self.used_incap_singles[i] = True

    def incap_single_in_use(self, i):
        if i not in self.incap_singles:
            raise ValueError('invalid incap_single index[%s] not in %s' % \
                    (i, self.incap_singles))
        return self.used_incap_singles[i]

    def use_twi_pin(self, i):
        if i not in self.twi_pins:
            raise ValueError('invalid twi_pin index[%s] not in %s' % \
                    (i, self.twi_pins))
        self.used_twi_pins[i] = True

    def twi_pin_in_use(self, i):
        if i not in self.twi_pins:
            raise ValueError('invalid twi_pin index[%s] not in %s' % \
                    (i, self.twi_pins))
        return self.used_twi_pins[i]

    def use_icsp(self):
        self.used_icsp = True

    def icsp_in_use(self):
        return self.used_icsp
