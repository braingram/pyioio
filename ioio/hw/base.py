#!/usr/bin/env python
"""
Hardware modules (for example: pwm, uart, etc...)
"""


def make_set(items, value=False):
    """
    items : (list, tuple, int, tuple of tuples, list of lists)
    """
    if callable(value):
        f = value
    else:
        f = lambda: value
    if isinstance(items, int):
        return dict([(k, f()) for k in range(items)])
    if isinstance(items, (tuple, list)):
        if len(items) == 0:
            return {}
        i = items[0]
        if isinstance(i, (tuple, list)):
            return dict([(tuple(k), False) for k in items])
        return dict([(k, f()) for k in items])
    raise ValueError("Invalid items %s" % items)


class HWModule(object):
    def __init__(self, pins, value=False):
        self.pins = make_set(pins, value)

    def free_pin(self, pin, free_value=None):
        self.pins[pin] = free_value

    def valid_pin(self, i):
        return i in self._pins

    def check_pin(self, i):
        if not self.valid_pin(self, i):
            raise ValueError("Invalid pin %i for %s" % (i, self))


class HWWithSubmodules(HWModule):
    """
    pins are either None or an key for the subs dict
    """
    def __init__(self, pins, subs=None, subclass=dict):
        HWModule.__init__(self, pins, None)
        if subs is None:
            subs = pins
        self._subclass = subclass
        self.subs = make_set(subs, self._subclass)

    def get_unused_submodule(self):
        for k in self.subs:
            if k not in self.pins.values():
                return k
        raise ValueError("No unused submodules: %s, %s" %
                         (self.pins, self.subs))

    def find_submodule(self, submodule):
        """
        If submodule is a key, return value from self.subs
        """
        if not isinstance(submodule, self._subclass):
            return self.subs[submodule]
        for k in self.subs:
            if self.subs[k] == submodule:
                return k

    def get_submodule_for_pin(self, pin):
        return self.pins[pin]

    def assign_pin(self, pin, index):
        if isinstance(index, self._subclass):
            index = self.find_submodule(self, index)
        self.pins[pin] = index
