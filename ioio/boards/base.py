#!/usr/bin/env python

from . import hwmodules


class Board(object):
    def __init__(self, protocol, pins, n_pwms, n_uarts, n_spis, incap_doubles,
            incap_singles, twi_pins, icsp_pins):
        self.pins = {
            'p_in': hwmodules.PinSet(pins['p_in']),
            'p_out': hwmodules.PinSet(pins['p_out']),
            'analog': hwmodules.PinSet(pins['analog']),
            'pwm': hwmodules.PWM(pins['p_out'], n_pwms),
            # TODO distinguish between p_in and p_out
            'uart': hwmodules.UART(pins['p_out'], n_uarts),
            'spi': hwmodules.SPI(pins['p_out'], n_spis),
            'incap_double': hwmodules.IncapDouble(pins['p_in'], incap_doubles),
            'incap_single': hwmodules.IncapSingle(pins['p_in'], incap_singles),
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
