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

    def free(self, pin):
        """
        Free a pin
        """
        # TODO check if pin is already configured
        # if so, unconfigure pin
        # TODO special cleanup for modules
        self.write_command('set_pin_digital_in', pin, 'floating')
        self.write_command('set_change_notify', pin, False)
        self.pins[pin] = None

    def digital_in(self, pin, state, notify=True, callback=None):
        """
        stat :
            0 : floating
            1 : up
            2 : down
        """
        self.check_pin(pin, 'digital_in')
        self.write_command('set_pin_digital_in', pin, state)
        self.write_command('set_change_notify', pin, notify)
        self.pins[pin] = 'digital_in'
        # TODO register callback

    def digital_out(self, pin, level, open_drain=False):
        self.check_pin(pin, 'digital_out')
        self.write_command('set_pin_digital_out', pin, level, open_drain)
        self.write_command('set_digital_out_level', pin, level)
        self.pins[pin] = 'digital_out'

    def analog_in(self, pin, enable=True, callback=None):
        self.check_pin(pin, 'analog')
        self.modules.analog.check_pin(pin)
        self.write_command('set_pin_analog_in', pin)
        self.write_command('set_analog_in_sampling', pin, enable)
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
        elif status == 2:  # already a pwm pin
            if sindex is None:
                sindex = self.modules.pwm.get_submodule_for_pin(pin)
                assert sindex is not None
            submodule = self.modules.pwm.find_submodule(sindex)
        else:
            raise ValueError("check_pin returned invalid status: %s" % status)

        if (freq is not None) and (submodule.frequency != freq):
            submodule.frequency = freq
            self.write_command('set_pwm_period', submodule.scale,
                               sindex, submodule.period)
        if duty is None:
            return
        pw, f = submodule.parse_duty_cycle(duty)
        self.write_command('set_pwm_duty_cycle', f, sindex, pw)

    def pulse_in(self, pin, *args, **kwargs):
        # TODO
        # set_pin_digial_in
        # set_pin_incap
        # incap_config
        pass

    def uart(self, *args, **kwargs):
        # TODO
        # set_pin_uart ...
        # uart_config
        # uart_data ...
        pass
