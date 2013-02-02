#!/usr/bin/env python
"""
see: firmware/app_layer_v1/protocol_defs.h
"""


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
