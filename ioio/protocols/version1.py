#!/usr/bin/env python
"""
see: firmware/app_layer_v1/protocol_defs.h
"""

import struct

from .base import Protocol


class Version1Responses(object):
    """
    This requires some 'state' to know how many analog channels to read
    """
    def __init__(self):
        self.mapping = {
            '\x00': self.establish_connection,
            '\x01': self.soft_reset,
            '\x02': self.check_interface_response,
            #'\x03':
            '\x04': self.report_digital_in_status,
            '\x05': self.report_periodic_digital_in_status,
            '\x06': self.set_change_notify,
            '\x07': self.register_periodic_digital_sampling,
            #'\x08' ... '\x0A'
            '\x0B': self.report_analog_in_status,
            '\x0C': self.report_analog_in_format,
            '\x0D': self.uart_status,
            '\x0E': self.uart_data,
            '\x0F': self.uart_report_tx_status,
            '\x10': self.spi_status,
            '\x11': self.spi_data,
            '\x12': self.spi_report_tx_status,
            '\x13': self.twi_status,
            '\x14': self.twi_result,
            '\x15': self.twi_report_tx_status,
            '\x16': self.icsp_report_rx_status,
            '\x17': self.icsp_result,
            #'\x18':
            #'\x19':
            '\x1A': self.icsp_config,
            '\x1B': self.incap_status,
            '\x1C': self.incap_report,
            '\x1D': self.soft_close,
        }

    def read(self, io):
        k = io.read(1)
        if k == '':
            return {}
        return self.mapping[k](io)

    def establish_connection(self, io):
        return {'name': 'establish_connection',
                'magic': io.read(4),
                'hardware_version': io.read(8),
                'board_version': io.read(8),
                'firmware_version': io.read(8)}

    def soft_reset(self, io):
        return {'name': 'soft_reset'}

    def check_interface_response(self, io):
        return {'name': 'check_interface_response',
                'supported': bool(0x01 & ord(io.read(1)))}

    def report_digital_in_status(self, io):
        b = io.read(1)
        return {'name': 'report_digital_in_status',
                'level': bool(0x01 & ord(b)),
                'pin': (ord(b) >> 2)}

    def report_periodic_digital_in_status(self, io):
        return {'name': 'report_periodic_digital_in_status',
                'size': ord(io.read(1))}

    def set_change_notify(self, io):
        b = io.read(1)
        return {'name': 'set_change_notify',
                'change': bool(0x01 & ord(b)),
                'pin': (ord(b) >> 2)}

    def register_periodic_digital_sampling(self, io):
        return {'name': 'register_periodic_digital_sampling',
                'pin': (0x3F & ord(io.read(1))),
                'freq_scale': io.read(1)}

    def report_analog_in_status(self, io):
        if not hasattr(self, 'analog_pins'):
            raise ValueError('missing analog_pins')
        pins = {}
        r = {'name': 'report_analog_in_status'}
        for p in self.analog_pins:
            header, high = io.read(2)
            pins[p] = ((ord(header) & 0x03) | (ord(high) << 2))
        r['pins'] = pins
        return r

    def report_analog_in_format(self, io):
        n = ord(io.read(1))
        self.analog_pins = [ord(b) for b in io.read(n)]
        return {'name': 'report_analog_in_format',
                'num_pins': n,
                'pins': self.analog_pins}

    def uart_status(self, io):
        b = io.read(1)
        return {'name': 'uart_status',
                'uart_num': (0x03 & ord(b)),
                'enabled': (0x80 & ord(b))}

    def uart_data(self, io):
        b = io.read(1)
        n = (0x3F & ord(b))
        return {'name': 'uart_data',
                'size': n,
                # TODO double check this
                'uart_num': (ord(b) >> 6),
                'data': io.read(n + 1)[:-1]}

    def uart_report_tx_status(self, io):
        b0, b1 = io.read(2)
        return {'name': 'uart_report_tx_status',
                'uart_num': (0x03 & ord(b0)),
                'bytes_to_add': ((ord(b0) >> 2) | (ord(b1) << 6))}

    def spi_status(self, io):
        b = io.read(1)
        return {'name': 'spi_status',
                'spi_num': (0x03 & ord(b)),
                'enabled': (0x80 & ord(b))}

    def spi_data(self, io):
        b = io.read(1)
        n = (0x3F & ord(b))
        return {'name': 'spi_data',
                'size': n,
                'spi_num': (ord(b) >> 6),
                'ss_pin': (0x3F & ord(io.read(1))),
                'data': io.read(n)}

    def spi_report_tx_status(self, io):
        b0, b1 = io.read(2)
        return {'name': 'spi_report_tx_status',
                'spi_num': (0x03 & ord(b0)),
                'bytes_to_add': ((ord(b0) >> 2) | (ord(b1) << 6))}

    def twi_status(self, io):
        b = io.read(1)
        return {'name': 'twi_status',
                'twi_num': (0x03 & ord(b)),
                'enabled': (0x80 & ord(b))}

    def twi_result(self, io):
        b0, b1 = io.read(2)
        n = ord(b1)
        return {'name': 'twi_result',
                'twi_num': (0x03 & ord(b0)),
                'size': n,
                'data': io.read(n)}

    def twi_report_tx_status(self, io):
        b0, b1 = io.read(2)
        return {'name': 'twi_report_tx_status',
                'twi_num': (0x03 & ord(b0)),
                'bytes_to_add': ((ord(b0) >> 2) | (ord(b1) << 6))}

    def icsp_report_rx_status(self, io):
        return {'name': 'icsp_report_rx_status',
                'bytes_to_add': struct.unpack('h', io.read(2))[0]}

    def icsp_result(self, io):
        return {'name': 'icsp_result',
                'reg': io.read(2)}

    def icsp_config(self, io):
        return {'name': 'icsp_config',
                'enable': (0x01 & ord(io.read(1)))}

    def incap_status(self, io):
        b = io.read(1)
        return {'name': 'incap_status',
                'incap_num': (0x0F & ord(b)),
                'enabled': bool((0x80 & ord(b)))}

    def incap_report(self, io):
        b = io.read(1)
        n = (ord(b) >> 6)
        if n == 0:
            n = 4
        return {'name': 'incap_report',
                'incap_num': (0x0F & ord(b)),
                'size': n,
                'length': io.read(n)}

    def soft_close(self, io):
        return {'name': 'soft_close'}


class Version1Commands(object):
    pull_states = {
        'floating': 0,
        'up': 1,
        'down': 2,
    }

    scale_codes = {
        '1': 0,
        '8': 3,
        '64': 2,
        '256': 1,
    }

    pulse_clocks = {
        '16MHz': 0,
        '2MHz': 1,
        '250kHz': 2,
        '62.5khz': 3,
    }

    pulse_modes = {
        'positive': 0,
        'negative': 1,
        'frequency': 2,
        'frequency4x': 3,
        'frequency16x': 4,
    }

    uart_directions = {
        'rx': 0,
        'tx': 1,
    }

    def write(self, interface, command, *args, **kwargs):
        if not hasattr(self, command):
            raise ValueError("Unknown command: %s" % command)
        interface.write(getattr(self, command)(*args, **kwargs))

    def hard_reset(self):
        return '\x00IOIO'

    def soft_reset(self):
        return '\x01'

    def check_interface(self, interface='IOIO0003'):
        assert isinstance(interface, str)
        assert len(interface) < 8
        return '\x02' + interface

    def set_pin_digital_out(self, pin, value=0, open_drain=1):
        assert isinstance(pin, int)
        return '\x03' + chr((pin << 2) |
                            ((0x01 & bool(value)) << 1) |
                            (0x01 & bool(open_drain)))

    def set_digital_out_level(self, pin, value=0):
        assert isinstance(pin, int)
        return '\x04' + chr((pin << 2) | (0x01 & bool(value)))

    def set_pin_digital_in(self, pin, pull):
        assert isinstance(pin, int)
        if isinstance(pull, (str, unicode)):
            if pull not in self.pull_states:
                raise ValueError("Unknown pull: %s not in %s" %
                                 (pull, self.pull_states))
            pull = self.pull_states[pull]
        return '\x05' + chr((pin << 2) | (0x03 & pull))

    def set_change_notify(self, pin, notify=True):
        assert isinstance(pin, int)
        return '\x06' + chr((pin << 2) | (0x01 & bool(notify)))

    def register_periodic_digital_sampling(self, pin, freq_scale=0):
        assert isinstance(pin, int)
        # TODO check/parse freq_scale
        return '\x07' + chr((pin << 2)) + chr(freq_scale)

    def set_pin_pwm(self, pin, pwm_num, enable=True):
        assert isinstance(pin, int)
        return '\x08' + chr((pin << 2)) + \
            chr((pwm_num << 4) | (0x01 & bool(enable)))

    def set_pwm_duty_cycle(self, fraction, pwm_num, duty_cycle):
        return '\x09' + chr((fraction << 6) | ((pwm_num & 0x0f) << 2)) + \
            struct.pack('h', duty_cycle)

    def set_pwm_period(self, scale, pwm_num, period):
        if isinstance(scale, (str, unicode)):
            if scale not in self.scale_codes:
                raise ValueError("Unknown scale: %s not in %s" %
                                 (scale, self.scale_codes))
            scale = self.scale_codes[scale]
        sl = ((scale & 0x01) << 7)
        sh = (scale & 0x02)
        return '\x0A' + chr(sl | ((pwm_num & 0x0f) << 3) | sh) + \
            struct.pack('h', period)

    def set_pin_analog_in(self, pin):
        assert isinstance(pin, int)
        return '\x0B' + chr(pin)

    def set_analog_in_sampling(self, pin, enable=True):
        assert isinstance(pin, int)
        return '\x0C' + chr(((0x01 & enable) << 7) | (0x3F & pin))

    def uart_config(self, uart_num, baud=9600, parity=0, two_stop_bits=0,
                    speed4x=0):
        return '\x0D' + \
            chr((parity << 6) | ((two_stop_bits & 0x01) << 5) |
                ((speed4x & 0x01) << 2) | (uart_num << 6)) + \
            struct.pack('h', baud)

    def uart_data(self, uart_num, data, size=None):
        assert isinstance(uart_num, int)
        assert isinstance(data, str)
        size = len(data) if size is None else size
        assert len(data) == size
        return '\x0E' + chr((size << 2) | (uart_num & 0x03)) + data

    def set_pin_uart(self, pin, uart_num, direction, enable=True):
        if isinstance(direction, (str, unicode)):
            if direction not in self.uart_directions:
                raise ValueError("Unknown direction: %s not in %s" %
                                 (direction, self.uart_directions))
            direction = self.uart_directions[direction]
        return '\x0F' + chr((pin << 2)) + \
            chr((uart_num << 6) |
                ((direction & 0x01) << 1) | (enable & 0x01))

    def spi_configure_master(self):
        """
        'spi_configure_master': packet('\x10',
            ('div', 3, 'i'),
            ('scale', 2, 'i'),
            ('spi_num', 2, 'i'),
            ('', 1),
            ('clk_pol', 1, 'b'),
            ('clk_edge', 1, 'b'),
            ('smp_end', 1, 'b'),
            ('', 5)
        """
        raise NotImplementedError

    def spi_master_request(self):
        """
        'spi_master_request': packet('\x11',
            ('ss_pin', 6, 'i'),
            ('spi_num', 2, 'i'),
            ('total_size', 6, 'i'),
            ('res_size_neq_total', 1, 'b'),
            ('data_size_neq_total', 1, 'b'),
            ('data_size', 8, 'i'),
            ('data', 'data_size', 'c')),
        """
        raise NotImplementedError

    def set_pin_spi(self):
        """
        'set_pin_spi': packet('\x12',
            ('pin', 6, 'i'),
            ('', 2),
            ('spi_num', 2, 'i'),
            ('mode', 2, 'i'),
            ('enable', 1, 'b'),
            ('', 3)),
        """
        raise NotImplementedError

    def twi_configure_master(self):
        """
        'i2c_configure_master': packet('\x13',
            ('i2c_num', 2, 'i'),
            ('', 3),
            ('rate', 2, 'i'),
            ('smbus_levels', 1, 'b')),
        """
        raise NotImplementedError

    def twi_write_read(self):
        """
        'i2c_write_read': packet('\x14',
            ('i2c_num', 2, 'i'),
            ('', 3),
            ('ten_bit_addr', 1, 'b'),
            ('addr_msb', 2, 'i'),
            ('addr_lsb', 8, 'i'),
            ('write_size', 8, 'i'),
            ('read_size', 8, 'i'),
            ('data', 'write_size', 'c')),
        """
        raise NotImplementedError

    def icsp_six(self):
        """
        'icsp_six': packet('\x16',
            ('inst', 24, 'c')),
        """
        raise NotImplementedError

    def icsp_regout(self):
        """
        'icsp_regout': packet('\x17'),
        """
        raise NotImplementedError

    def icsp_prog_enter(self):
        """
        'icsp_prog_enter': packet('\x18'),
        """
        raise NotImplementedError

    def icsp_prog_exit(self):
        """
        'icsp_prog_exit': packet('\x19'),
        """
        raise NotImplementedError

    def icsp_config(self):
        """
        'icsp_config': packet('\x1A',
            ('enable', 1, 'b'),
            ('', 7)),
        """
        raise NotImplementedError

    def incap_config(self, incap_num, clock, mode, double):
        if isinstance(clock, (str, unicode)):
            if clock not in self.pulse_clocks:
                raise ValueError("Unknown clock [%s] not in %s" %
                                 (clock, self.pulse_clocks))
            clock = self.pulse_clocks[clock]
        if isinstance(mode, (str, unicode)):
            if mode not in self.pulse_modes:
                raise ValueError("Unknown mode [%s] not in %s" %
                                 (mode, self.pulse_modes))
            mode = self.pulse_modes[mode]
        return '\x1B' + chr(incap_num) + \
            chr(((0x01 & double) << 7) | (mode << 3) | clock)

    def set_pin_incap(self, pin, incap_num, enable=True):
        return '\x1C' + chr(pin) + \
            chr(((0x01 & enable) << 7) | incap_num)

    def soft_close(self):
        return '\x1D'


class Version1Protocol(Protocol):
    def __init__(self, interface, connection_packet):
        Protocol.__init__(self, interface, Version1Commands(),
                          Version1Responses())
        self.connection_packet = connection_packet
