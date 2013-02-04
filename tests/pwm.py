#!/usr/bin/env python

import logging
import time

import ioio

logging.basicConfig(level=logging.DEBUG)

port = '/dev/ttyACM0'
pin = 0
pnum = 0

frequency = 100

clk = 16000000
scales = [1, 8, 64, 256]
scale_encodings = {
        1: 0,
        8: 3,
        64: 2,
        256: 1,
        }
max_period = 2 ** 16  # 65536


def find_scale_and_period(freq):
    for s in scales:
        p = (clk / s) / float(freq)
        if p <= max_period:
            return s, p
    raise ValueError("Frequency too low: %s" % freq)


def duty_cycle_to_clocks(period, dc):
    return period * dc


#def calc_base_usec(scale_index):
#    return 1000000. / (clk / float(scales[scale_index]))


#def dc_usec_to_clocks(pulse_width_usec, base_usec):
#    return pulse_width_usec / base_usec


def dc_in_clocks(pulse_width_clocks):
    pulse_width_clocks -= 1
    if (pulse_width_clocks < 1):
        pw = 0
        fraction = 0
    else:
        pw = int(pulse_width_clocks)
        fraction = (int(pulse_width_clocks * 4) & 0x03)
    return pw, fraction

try:
    import qarg
    ns = qarg.get('interface[str=%s,pin[int=%i' % \
            (port, pin))
    port = ns.interface
    pin = ns.pin
except ImportError:
    print "please install qarg for argument parsing: github.com/braingram/qarg"


def pwm_params(freq, duty_cycle):
    # dc (in clocks)
    # scale
    # period
    scale, period = find_scale_and_period(freq)
    dcc = duty_cycle_to_clocks(period, duty_cycle)
    pw, fraction = dc_in_clocks(dcc)
    se = scale_encodings[scale]
    sl = (se & 0x01)
    sh = (se & 0x02) >> 1
    return period - 1, sl, sh, pw, fraction


i = ioio.IOIO(port, timeout=0.01)

i.write('set_pin_digital_out', pin=pin, open_drain=False, value=False)
i.write('set_pin_pwm', pin=pin, enable=True, pwm_num=pnum)
steps = 100
first = True
try:
    while True:
        for direction in xrange(2):
            for dci in xrange(steps):
                dc = dci / float(steps)
                if direction:
                    dc = 1 - dc
                #print "Duty Cycle: %s" % dc
                period, sl, sh, pw, fraction = pwm_params(frequency, dc)
                if pw > period:
                    pw = period
                #print period, sl, sh, pw, fraction
                if first:
                    i.write('set_pwm_period', pwm_num=pnum, scale_l=sl, \
                            scale_h=sh, period=period)
                    first = False
                i.write('set_pwm_duty_cycle', pwm_num=pnum, dc=pw, \
                        fraction=fraction)
                r = i.read()
                if r != {}:
                    print r
                time.sleep(0.1)
        #i.write('set_pin_pwm', pin=pin, enable=False, pwm_num=pnum)
        #first = False
        #print "pausing..."
        #time.sleep(0.5)
except KeyboardInterrupt:
    pass

# need to set
# - set_pwm_duty_cycle
#   - fraction : 2
#       fraction of the duty cycle (.
#   - dc : 16
# - set_pwm_period
#   - scale_l : 1
#   - scale_h : 1
#   - period : 16
#_ = raw_input('press enter to exit...')

i.write('soft_reset')
del i
