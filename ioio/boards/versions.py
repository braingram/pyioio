#!/usr/bin/env python
"""
pin defs: p.in p.out analog
peripherals:
    pwm
    uart
    spi
    incap(pulse_in)
    twi
    icsp
check valid pin/pwm/uart/spi...
"""

from .base import Board

# each pin can be
# - p.out
# - p.in
# - analog
# - uart
IOIO0002_pins = dict(
        p_in=(0, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 27, 28, 29, 30,
            31, 32, 34, 35, 36, 37, 38, 39, 40, 45, 46, 47, 48),
        p_out=(0, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 27, 28, 29, 30,
            31, 32, 34, 35, 36, 37, 38, 39, 40, 45, 46, 47, 48),
        analog=(31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
            45, 46),
        )

# pins,
# n_pwms, n_uarts, n_spis, incap_doubles, incap_singles, twi_pins,
# icsp_pins
IOIO0002 = (IOIO0002_pins,
    9, 4, 3, (0, 2, 4), (6, 7, 8), ((4, 5), (47, 48), (26, 25)),
    ((36, 37, 38), ))

IOIO0003 = IOIO0002

IOIO0004_pins = dict(
        p_in=(1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 27, 28,
            29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 45, 46),
        p_out=(1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 27, 28,
            29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 45, 46),
        analog=(31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
            43, 44, 45, 46),
        )

IOIO0004 = (IOIO0004_pins,
    9, 4, 3, (0, 2, 4), (6, 7, 8), ((4, 5), (47, 48), (26, 25)),
    ((36, 37, 38), ))


class SPRK0015(Board):
    def __init__(self, protocol):
        Board.__init__(self, protocol, *IOIO0003)


class SPRK0016(Board):
    def __init__(self, protocol):
        Board.__init__(self, protocol, *IOIO0003)


class MINT0010(Board):
    def __init__(self, protocol):
        Board.__init__(self, protocol, *IOIO0003)


class SPRK0020(Board):
    def __init__(self, protocol):
        Board.__init__(self, protocol, *IOIO0004)
