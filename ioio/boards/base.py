#!/usr/bin/env python

from . import hwmodules
from .. import utils


class Modules(object):
    pass


class Board(object):
    def __init__(self, protocol, n_pins, pins, n_pwms, n_uarts, n_spis, \
            incap_doubles, incap_singles, twi_pins, icsp_pins):
        utils.shadow(protocol, self)

        self.pins = dict([(i, None) for i in xrange(n_pins)])
        self.modules = Modules()

        # singles
        #self.digital_in = hwmodules.DIGITALIN(self.n_pins)
        #self.digital_out = hwmodules.DIGITALOUT(self.n_pins)
        #self.analog = hwmodules.ANALOG(pins['analog'])
        self.modules.analog = hwmodules.Analog(pins['analog'])
        #self.free = hwmodules.FREE()

        # multiples
        self.modules.pwm = hwmodules.PWM(pins['p_out'], n_pwms)
        self.modules.uart = hwmodules.UART(pins['p_out'], n_uarts)
        self.modules.spi = hwmodules.SPI(pins['p_out'], n_spis)
        self.modules.pulse_double = hwmodules.PulseDouble(pins['p_in'], \
                incap_doubles)
        self.modules.pulse_single = hwmodules.PulseSingle(pins['p_in'], \
                incap_singles)
        self.modules.twi = hwmodules.TWI(twi_pins)

        # TODO icsp
        #self.icsp = hwmodules.ICSP(icsp_pins)

    def free(self, pin):
        """
        Free a pin
        """
        # TODO check if pin is already configured
        # if so, unconfigure pin
        self.write_command('set_pin_digital_in', pin, 0)  # floating
        self.write_command('set_change_notify', pin, False)

    def digital_in(self, pin, state, notify=True, callback=None):
        """
        stat :
            0 : floating
            1 : up
            2 : down
        """
        # TODO check pin
        self.write_command('set_pin_digital_in', pin, state)
        self.write_command('set_change_notify', pin, notify)
        # TODO register callback

    def digital_out(self, pin, level, open_drain=False):
        # TODO check if pin is already configured
        self.write_command('set_pin_digital_out', pin, level, open_drain)

    def analog_in(self, pin, enable=True, callback=None):
        # TODO check if pin is already configured
        self.modules.analog.check_pin(pin)
        self.write_command('set_pin_analog_in', pin)
        self.write_command('set_analog_in_sampling', pin, enable)
        # TODO register callback

    def pwm(self, pin, *args, **kwargs):
        # TODO check if pin is already configured
        # if so, get existing pwm module

        self.modules.pwm.check_pin(pin)

        module = None
        if not len(args):
            raise ValueError()
        if isinstance(args[0], hwmodules.PWM):
            # module is args[0]
            module = args[0]
            args = args[1:]
            # additiona args & kwargs for setting up the module
            pass
        else:
            # make new module
            module = self.modules.pwm.next()
            # setup with args & kwargs
            pass
        # finally, setup the pin
        # set_pin_digital_out : pin, 0, open_drain
        # set_pin_pwm : pin, enable, pwm_num
        # set_pwm_period : pwm_num, scale_l, scale_h, period
        # set_pwm_duty_cycle: pwm_num, dc, fraction
        pass

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
