#!/usr/bin/env python

from .. import utils
from .. import hw


class Modules(object):
    pass


class Board(object):
    def __init__(self, protocol, n_pins, pins, n_pwms, n_uarts, n_spis,
                 incap_doubles, incap_singles, twi_pins, icsp_pins):
        utils.shadow(protocol, self)

        self.pins = dict([(i, None) for i in xrange(n_pins)])
        self.modules = Modules()

        # singles
        self.modules.analog = hw.Analog(pins['analog'])

        # multiples
        self.modules.pwm = hw.PWM(pins['p_out'], n_pwms)
        self.modules.uart = hw.UART(pins['p_out'], n_uarts)
        self.modules.spi = hw.SPI(pins['p_out'], n_spis)
        self.modules.pulse_double = hw.PulseDouble(pins['p_in'],
                                                   incap_doubles)
        self.modules.pulse_single = hw.PulseSingle(pins['p_in'],
                                                   incap_singles)
        self.modules.twi = hw.TWI(twi_pins)

        # TODO icsp
        #self.icsp = hwmodules.ICSP(icsp_pins)

    def soft_reset(self):
        raise NotImplementedError

    def check_pin(self, pin, function, throw=True):
        if self.pins[pin] is None:
            return 1
        if self.pins[pin] == function:
            return 2
        if throw:
            raise IOError("Attempt to use configured pin %i [%s] as %s" %
                          (pin, self.pins[pin], function))
        return 0

    def free_pin(self, pin):
        """
        Free a pin
        """
        # TODO check if pin is already configured
        # if so, unconfigure pin
        # TODO special cleanup for modules
        self.write_command('set_pin_digital_in', pin, 'floating')
        self.write_command('set_change_notify', pin, False)
        self.pins[pin] = None

    def assign_pin(self, pin, function):
        self.pins[pin] = function

    def digital_in(self, pin, state='up', notify=True, callback=None):
        """
        state can be 'floating', 'up', 'down', or 0, 1, 2
        """
        self.check_pin(pin, 'digital_in')
        self.write_command('set_pin_digital_in', pin, state)
        self.write_command('set_change_notify', pin, notify)
        self.assign_pin(pin, 'digital_in')
        # TODO register callback

    def digital_out(self, pin, level, open_drain=False):
        status = self.check_pin(pin, 'digital_out')
        if status == 1:
            self.write_command('set_pin_digital_out', pin, level, open_drain)
            self.assign_pin(pin, 'digital_out')
        self.write_command('set_digital_out_level', pin, level)

    def analog_in(self, pin, enable=True, callback=None):
        self.check_pin(pin, 'analog')
        self.modules.analog.check_pin(pin)
        self.write_command('set_pin_analog_in', pin)
        self.write_command('set_analog_in_sampling', pin, enable)
        self.assign_pin(pin, 'analog')
        # TODO register callback

    def pwm(self, pin, duty=None, freq=None, sindex=None, open_drain=False):
        """
        possible args:
            freq, duty
            submodule (of PWM)
            freq, pulse_width  # TODO this later
        optional args:
            open_drain
        """
        self.modules.pwm.check_pin(pin)
        status = self.check_pin(pin, 'pwm')
        if status == 1:  # previously unassigned
            self.write_command('set_pin_digital_out', pin, 0, open_drain)
            if sindex is None:
                # get a new sindex
                sindex = self.modules.pwm.get_unused_submodule()
            submodule = self.modules.pwm.find_submodule(sindex)
            self.write_command('set_pin_pwm', pin, sindex, enable=True)
            self.modules.pwm.assign_pin(pin, sindex)
            self.assign_pin(pin, 'pwm')
        elif status == 2:  # already a pwm pin
            if sindex is None:
                sindex = self.modules.pwm.get_submodule_for_pin(pin)
                assert sindex is not None
            submodule = self.modules.pwm.find_submodule(sindex)
        else:
            raise ValueError("check_pin returned invalid status: %s" % status)

        self.modules.pwm.assign_pin(pin, sindex)

        if (freq is not None) and (submodule.frequency != freq):
            submodule.frequency = freq
            self.write_command('set_pwm_period', submodule.scale,
                               sindex, submodule.period)
        if duty is None:
            return
        pw, f = submodule.parse_duty_cycle(duty)
        self.write_command('set_pwm_duty_cycle', f, sindex, pw)

    def pulse_in(self, pin, clock=None, mode=None,
                 state='up', double=False, sindex=None):
        if double:
            hwm = self.modules.pulse_double
        else:
            hwm = self.modules.pulse_single
        # also test single
        hwm.check_pin(pin)
        status = self.check_pin(pin, 'pulse_in')
        if status == 1:  # previously unassigned
            if sindex is None:
                sindex = hwm.get_unused_submodule()
            self.write_command('set_pin_digital_in', pin, state)
            self.assign_pin(pin, 'pulse_in')
        elif status == 2:  # already a pwm pin
            if sindex is None:
                sindex = hwm.get_submodule_for_pin(pin)
                assert sindex is not None
        else:
            raise ValueError("Unknown pin status %s for %s" %
                             (status, pin))

        hwm.assign_pin(pin, sindex)
        self.write_command('set_pin_incap', pin, sindex)

        # this function might be called with pin & sindex just to change index
        if (clock is not None) and (mode is not None):
            self.write_command('incap_config', sindex, clock, mode, double)

    def uart(self, **kwargs):
        """
        rx_pin : int or None
        rx_pin_statestate : 'floating', 'up', 'down'
        tx_pin : int or None
        tx_pin_open_drain : True/False
        sindex : int or None
        rate, parity, two_stop_bits, speed4x : see uart_config
        data : string
        """
        rx_pin = kwargs.get('rx_pin', None)
        tx_pin = kwargs.get('tx_pin', None)
        rx_pin_state = kwargs.get('rx_pin_state', 'up')
        tx_pin_open_drain = kwargs.get('tx_pin_open_drain', False)
        assert not((rx_pin is None) and (tx_pin is None))
        status = self.check_pin(rx_pin, 'uart')
        status = self.check_pin(tx_pin, 'uart')
        assert status == status
        sindex = kwargs.get('sindex', None)
        if status == 1:
            if sindex is None:
                sindex = self.modules.uart.get_unused_submodule()
            if rx_pin is not None:
                self.write_command('set_pin_digital_in', rx_pin, rx_pin_state)
                self.write_command('set_pin_uart', rx_pin, sindex, 'rx')
                self.assign_pin(rx_pin, 'uart')
                self.modules.uart.assign_pin(rx_pin, sindex)
            if tx_pin is not None:
                self.write_command('set_pin_digital_out', tx_pin,
                                   0, tx_pin_open_drain)
                self.write_command('set_pin_uart', tx_pin, sindex, 'tx')
                self.assign_pin(tx_pin, 'uart')
                self.modules.uart.assign_pin(tx_pin, sindex)
        elif status == 2:  # old
            if sindex is None:
                if (rx_pin is not None) and (tx_pin is not None):
                    rx_sindex = self.modules.uart.get_submodule_for_pin(rx_pin)
                    tx_sindex = self.modules.uart.get_submodule_for_pin(tx_pin)
                    assert rx_sindex == tx_sindex
                    assert rx_sindex is not None
                    sindex = rx_sindex
                elif rx_pin is not None:
                    rx_sindex = self.modules.uart.get_submodule_for_pin(rx_pin)
                    sindex = rx_sindex
                else:
                    tx_sindex = self.modules.uart.get_submodule_for_pin(tx_pin)
                    sindex = tx_sindex
        else:
            raise ValueError("Unknown pin status %s for %s" %
                             (status, rx_pin))

        # check current configuration
        cfg = dict([(k, kwargs[k]) for k in ('baud', 'parity',
                                             'two_stop_bits', 'speed4x')
                    if k in kwargs])
        submodule = self.modules.uart.find_submodule(sindex)
        if submodule.check_config(cfg):
            submodule.set_config(cfg)
            self.write_command('uart_config', sindex, **submodule.get_config())

        if 'data' in kwargs:
            self.write_command('uart_data', sindex, kwargs['data'])
