#!/usr/bin/env python

from .base import Board


class OTG(Board):
    def __init__(self, protocol):
        Board.__init__(self, protocol)
