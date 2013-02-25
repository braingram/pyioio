#!/usr/bin/env python
"""
Hardware modules (for example: pwm, uart, etc...)
"""


def make_set(items, value=False):
    """
    items : (list, tuple, int, tuple of tuples, list of lists)
    """
    if isinstance(items, int):
        return dict([(k, False) for k in range(items)])
    if isinstance(items, (tuple, list)):
        if len(items) == 0:
            return {}
        i = items[0]
        if isinstance(i, (tuple, list)):
            return dict([(tuple(k), False) for k in items])
        if callable(value):
            f = value
        else:
            f = lambda: value
        return dict([(k, f()) for k in items])
    raise ValueError("Invalid items %s" % items)


class HWModule(object):
    def __init__(self, pins):
        self.valid_pins = make_set(pins)

    def valid_pin(self, i):
        return i in self.valid_pins

    def check_pin(self, i):
        if not self.valid_pin(self, i):
            raise ValueError("Invalid pin %i for %s" % (i, self))

    def set_pin(self, ioio, i, *args, **kwargs):
        self.check_pin(i)


class HWWithSubmodules(HWModule):
    def __init__(self, pins, subs=None):
        HWModule.__init__(self, pins)
        if subs is None:
            subs = len(pins)
        self.subs = make_set(subs, dict)


class Analog(HWModule):
    pass


class PWM(HWWithSubmodules):
    clock = 16000000
    scales = [1, 8, 64, 256]
    sclae_encodings = {
        1: 0,
        8: 3,
        64: 2,
        256: 1,
    }
    max_period = 65536


class UART(HWWithSubmodules):
    pass


class SPI(HWWithSubmodules):
    # TODO
    pass


class Incap(HWWithSubmodules):
    clock = {
        '16MHz': 0,
        '2MHz': 1,
        '250kHz': 2,
        '62.5kHz': 3,
    }
    mode = {
        'positive': 0,
        'negative': 1,
        'frequency': 2,
        'frequency4x': 3,
        'frequency16x': 4,
    }


class PulseDouble(HWWithSubmodules):
    double = True


class PulseSingle(HWWithSubmodules):
    double = False


class TWI(HWWithSubmodules):
    # TODO
    pass


class ICSP(HWWithSubmodules):
    # TODO
    pass
