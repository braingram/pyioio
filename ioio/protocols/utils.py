#!/usr/bin/env python
"""
see: firmware/app_layer_v1/protocol_defs.h
"""

import math


def packet(char, *args):
    """
    args are bit ordered right to left so
        ('a', 1), ('b', 3) = bbba
    set arg[1] = 0 for variable length arguments
    """
    bitcount = 0
    keys = []
    for arg in args:
        if len(arg) == 2:
            k, n = arg
            t = None
        elif len(arg) == 3:
            k, n, t = arg
        else:
            raise ValueError('Invalid packet arg: %r, %s, ' \
                'must be len == 2 or 3' % (char, arg))
	if not isinstance(k, str):
            raise ValueError('arg[0] must be a string: %r, %s' \
                % (char, arg))
        if isinstance(n, int):
            if n <= 0:
                raise ValueError('Invalid number of bits: %r, %s' \
                    % (char, arg))
            nb = n
        elif isinstance(n, str):
            if n not in keys:
                raise ValueError('Invalid inter-packet reference: %r, %s' \
                    % (char, arg))
            nb = 0
        else:
            raise ValueError('Invalid nbits type: %r, %s' % (char, arg))
        keys.append(k)
        if (k != '') and (not (isinstance(t, str) and (t in 'bic'))):
            raise ValueError('arg[2] must be a valid type [b/i/c]: %r, %s' \
                % (char, arg))
        bitcount += nb
    if not ((bitcount == 0) or (bitcount % 8 == 0)):
        raise ValueError('Invalid bitcount[%s] for packet: %r, %s' %
                (bitcount, char, args))
    nbytes = int(bitcount / 8)
    return dict(char=char, args=args, nbytes=nbytes)


def extract(dtype, nbits, data, bytei, biti):
    if dtype == 'b':  # extract boolean
        return bool(ord(data[bytei]) & (0x80 >> biti))
    elif dtype == 'i':  # extract integer
        if nbits == 1:
            return int(extract('b', nbits, data, bytei, biti))
        r = 0
        for i in xrange(nbits):
            B = bytei + int((i + biti) // 8)
            b = (i + biti) % 8
            r = (r << 1)
            if extract('b', 1, data, B, b):
                r |= 0x01
        return r
    elif dtype == 'c':  # extract character array/string
        if biti == 0:  # on a byte boundry
            return data[bytei:bytei + (nbits // 8)]
        else:
            raise NotImplementedError("Cannot extract chr within a byte")
    else:
        raise ValueError("Unknown type: %s [%s, %s, %s, %s]" %
                (dtype, nbits, data, bytei, biti))


def to_char_lookup(packets):
    l = {}
    for (k, v) in packets.iteritems():
        l[v['char']] = v
        l[v['char']]['name'] = k
    if len(l) != len(packets):
        raise ValueError("Failed to create character lookup for packets")
    return l


def read_response(interface, response_chars):
    """
    Read a response
    """
    rtype = interface.read(1)
    if (rtype not in response_chars):
        raise ValueError("Unknown response type: %r" % rtype)
    resp = response_chars[rtype]
    result = {'name': resp['name']}
    if len(resp['args']):
        data = interface.read(resp['nbytes'])
        bytei = 0
        biti = 0
        for arg in resp['args']:
            if isinstance(arg[1], str):
                nb = result[arg[1]]
            else:
                nb = arg[1]
            if arg[0] != '':
                result[arg[0]] = extract(arg[2], nb,
                        data, bytei, biti)
            biti += nb
            if biti > 7:
                bytei += int(biti // 8)
                biti = biti % 8
    # TODO packets with extra data
    return result


def package(spec, data, result=None, biti=0):
    if len(spec) == 0:
        return []
    if len(spec) > 1:
        if result is None:
            r = []
        else:
            r = result
        for item in spec:
            r = package((item, ), data, r, biti)
            nb = item[1]
            if isinstance(nb, str):
                nb = data[item[0]]
            biti += nb
        return r
    if result is None:
        result = []
    item = spec[0]
    name = item[0]
    nb = item[1]
    if isinstance(nb, str):
        nb = data[name]
    if name == '':
        # add a bunch of 0s
        # test if a new byte is needed
        nB = math.ceil((biti + nb) / 8.)
        while nB > len(result):
            result += ['\x00',]
        return result
    datum = data[name]
    dtype = item[2]
    print datum, type(datum)
    B, b = divmod(biti, 8)
    #if isinstance(datum, str):
    if dtype == 'c':
        data = str(datum)
        if b != 0:
            raise NotImplementedError('Can only add full chars')
        if len(datum) != int(nb // 8):
            raise ValueError('Invalid datum length %s expected %s' % \
                (len(datum), int(nb // 8)))
        # add characters
        return result + list(datum)
    # test if a new byte is needed
    nB = math.ceil((biti + nb) / 8.)
    while nB > len(result):
        result += ['\x00', ]
    #if isinstance(datum, bool):
    if dtype == 'b':
        datum = bool(datum)
        # flip 1 bit
        if datum:
            result[B] = chr(ord(result[B]) | (0x80 >> b))
        return result
    # test bool first as True isinstance of int
    #if isinstance(datum, int):
    if dtype == 'i':
        datum = int(datum)
        # flip many bits
        if (nb > 8):
            raise NotImplementedError('TODO')
        if datum:
            result[B] = chr(ord(result[B]) | (datum << (8 - b - nb)))
        return result
    raise ValueError('Invalid datum type: %s' % datum)


def write_command(interface, commands, name, **kwargs):
    if name not in commands:
        raise ValueError('Unknown command: %s' % name)
    cmd = commands[name]
    payload = [cmd['char'],]
    payload += package(cmd['args'], kwargs)
    interface.write(''.join(payload))
