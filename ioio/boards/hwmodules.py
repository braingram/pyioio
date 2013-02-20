#!/usr/bin/env python
"""
Hardware modules (for example: pwm, uart, etc...)
"""


def make_set(items):
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
        return dict([(k, False) for k in items])
    raise ValueError("Invalid items %s" % items)


class HWSet(object):
    def __init__(self, items):
        self.items = make_set(items)

    def valid(self, i):
        return i in self.items

    def item(self, i, value=None):
        if not self.valid(i):
            raise ValueError("Invalid i[%s] not in %s" % \
                (i, self.items))
        if value is None:
            return self.items[i]
        if value not in (True, False):
            raise ValueError("Invalid value %s" % value)
        self.items[i] = value

    def __len__(self):
        return len(self.items)

    def available(self, exclude=None):
        """
        get next available item or None if none are available
        """
        if exclude is None:
            exclude = ()
        for i in self.items:
            if (not self.items[i]) and (i not in exclude):
                return i
        return None


class PinSet(HWSet):
    pull = {
        'floating': 0,
        'up': 1,
        'down': 2,
    }
    def __init__(self, pins):
        HWSet.__init__(self, pins)

    valid_pin = valid
    pin = item
    available_pin = available


class HWModule(HWSet):
    def __init__(self, pins, indices):
        HWSet.__init__(self, indices)
        self.pins = pins
        # settings for each item
        self.settings = {}

    def valid_pin(self, i):
        return self.pins.valid(i)

    def pin(self, i, value=None):
        return self.pins.item(i, value)


class PWM(HWModule):
    clock = 16000000
    scales = [1, 8, 64, 256]
    sclae_encodings = {
        1: 0,
        8: 3,
        64: 2,
        256: 1,
    }
    max_period = 65536


class UART(HWModule):
    pass


class SPI(HWModule):
    # TODO
    pass


class Incap(HWModule):
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


class IncapDouble(HWModule):
    double = True


class IncapSingle(HWModule):
    double = False


class TWI(HWModule):
    # TODO
    pass


class ICSP(HWModule):
    # TODO
    pass
