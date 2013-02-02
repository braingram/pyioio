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
    for arg in args:
        if not(len(arg) > 1 and isinstance(arg[0], str) and
                isinstance(arg[1], int) and arg[1] >= 0):
            raise ValueError('Invalid packet args: %r, %s' % (char, args))
        if len(args) == 2 and (not args[0] == ''):
            raise ValueError('Packet arg missing type: %r, %s' % (char, arg))
        bitcount += arg[1]
    if not ((bitcount == 0) or (bitcount % 8 == 0)):
        raise ValueError('Invalid bitcount[%s] for packet: %r, %s' %
                (bitcount, char, args))
    nbytes = int(bitcount / 8)
    return dict(char=char, args=args, nbytes=nbytes)


def extract(dtype, nbits, data, bytei, biti):
    #TODO TEST
    if dtype == 'b':  # extract boolean
        return bool(data[bytei] & (0x80 >> biti))
    elif dtype == 'i':  # extract integer
        if nbits == 1:
            return int(extract('b', nbits, data, bytei, biti))
        r = 0
        for i in xrange(nbits):
            B = bytei + int((i + biti) // 8)
            b = (i + biti) % 8
            c = data[B]
            m = (0x80 >> (b - 1))
            r = (r & (c & m))
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


class Protocol(object):
    def __init__(self, commands, responses):
        self.commands = commands
        self._command_chars = to_char_lookup(commands)
        self.respones = responses
        self._response_chars = to_char_lookup(responses)

    def connect(self):
        raise NotImplementedError("Overload Protocol.connect")

    def disconnect(self):
        raise NotImplementedError("Overload Protocol.disconnect")

    def read(self, nbytes):
        raise NotImplementedError("Overload Protocol.read")

    def write(self, data):
        raise NotImplementedError("Overload Protocol.write")

    def read_packet(self):
        """
        Read a response
        """
        rtype = self.read(1)
        if (rtype not in self._response_chars):
            raise ValueError("Unknown response type: %r" % rtype)
        resp = self._response_chars[rtype]
        result = {'name': resp['name']}
        if len(resp['args']):
            data = self.read(resp['nbytes'])
            bytei = 0
            biti = 0
            # TODO packets with variable length data
            for arg in resp['args']:
                if arg[0] != '':
                    if arg[1] == 0:
                        raise NotImplementedError(
                                "Cannot process variable length data packets")
                    result[arg[0]] = extract(arg[2], arg[1],
                            data, bytei, biti)
                biti += arg[1]
                if biti > 7:
                    bytei += int(biti // 8)
                    biti = biti % 8
        # TODO packets with extra data
        return result

    def write_packet(self, name, **kargs):
        pass
