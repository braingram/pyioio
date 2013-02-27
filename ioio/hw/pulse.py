#!/usr/bin/env python

from base import HWWithSubmodules


class PulseDouble(HWWithSubmodules):
    double = True


class PulseSingle(HWWithSubmodules):
    double = False
