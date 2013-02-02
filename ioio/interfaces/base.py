#!/usr/bin/env python


class Interface(object):
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def read(self, nbytes):
        raise NotImplementedError('Override Interface.read')

    def write(self, data):
        raise NotImplementedError('Override Interface.read')
