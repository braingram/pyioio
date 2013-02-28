#!/usr/bin/env python

from base import HWWithSubmodules


class PulseDoubleSubmodule(object):
    double = True

    def __init__(self):
        self.reset()

    def reset(self):
        self.clock = '250kHz'
        self.mode = 'negative'
        self.pull = 'up'


class PulseSingleSubmodule(PulseDoubleSubmodule):
    double = False


class PulseDouble(HWWithSubmodules):
    def __init__(self, pins, subs=None):
        HWWithSubmodules.__init__(self, pins, subs, PulseDoubleSubmodule)


class PulseSingle(HWWithSubmodules):
    def __init__(self, pins, subs=None):
        HWWithSubmodules.__init__(self, pins, subs, PulseSingleSubmodule)
