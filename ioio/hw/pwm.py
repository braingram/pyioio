#!/usr/bin/env python


from base import HWWithSubmodules


def find_scale_and_period(frequency, scales, clock, max_period):
    for s in scales:
        p = (clock / s) / float(frequency)
        if p <= max_period:
            return s, p
    raise ValueError("Frequency too low: %s" % frequency)


def duty_cycle_in_clocks(period, duty_cycle):
    pulse_width_clocks = period * duty_cycle
    pulse_width_clocks -= 1
    if (pulse_width_clocks < 1):
        pw = 0
        fraction = 0
    else:
        pw = int(pulse_width_clocks)
        fraction = (int(pulse_width_clocks * 4) & 0x03)
    return pw, fraction


class PWMSubModule(object):
    clock = 16000000
    scales = [1, 8, 64, 256]
    max_period = 65536

    def __init__(self):
        self.set_frequency(100)

    def get_frequency(self):
        return self._freq

    def set_frequency(self, freq):
        self._freq = freq
        self.scale, self.period = \
            find_scale_and_period(self._freq,
                                  self.scales, self.clock,
                                  self.max_period)

    frequency = property(get_frequency, set_frequency)

    def parse_duty_cycle(self, dc):
        """
        Return pulse_width & fraction
        """
        return duty_cycle_in_clocks(self.period, dc)


class PWM(HWWithSubmodules):
    def __init__(self, pins, subs=None):
        HWWithSubmodules.__init__(self, pins, subs, PWMSubModule)
