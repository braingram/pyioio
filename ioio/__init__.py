#!/usr/bin/env python
"""
Each IOIO contains:
    - protocol : protocol version (packet spec)
    - board : physical hardware (pin spec)
    - interface : communication interface
"""

import threading
import time

from . import boards
from . import interfaces
from . import protocols


class IOIO(object):
    """
    Main IOIO class

    Contains
        interface : communication interface
        protocol : packet spec
        board : hardware/pin spec
    """
    def __init__(self, port, **kwargs):
        """
        Construct a connection
        """
        self.port = port
        self.interface = interfaces.find(port, **kwargs)
        self.protocol = protocols.find(self.interface)
        self.board = boards.find(self.protocol)

    def read(self):
        return self.protocol.read_response(self.interface)

    def write(self, name, **kwargs):
        self.protocol.write_command(self.interface, name, **kwargs)


class ThreadedIOIO(IOIO):
    def __init__(self, port, **kwargs):
        self.timeout = kwargs.get('timeout', 0.1)
        kwargs['timeout'] = self.timeout
        IOIO.__init__(self, port, **kwargs)
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def read(self):
        self.lock.acquire()
        r = IOIO.read(self)
        self.lock.release()
        return r

    def write(self, name, **kwargs):
        self.lock.acquire()
        IOIO.write(self, name, **kwargs)
        self.lock.release()

    def start_updating(self, callback):
        def update(f, to, callback, stop):
            while not stop.is_set():
                r = f()
                if r != {}:
                    callback(r)
                else:
                    time.sleep(to)

        self.stop_event.clear()
        self.update_thread = threading.Thread(target=update, \
            args=(self.read, self.timeout, \
                callback, self.stop_event))
        self.update_thread.start()

    def stop_updating(self):
        if not hasattr(self, 'update_thread'):
            return
        print "stopping thread"
        self.stop_event.set()
        self.update_thread.join()

    def __del__(self):
        self.stop_updating()
        self.interface.disconnect()
        if hasattr(IOIO, '__del__'):
            IOIO.__del__(self)


__all__ = ['IOIO']
