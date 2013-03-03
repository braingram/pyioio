#!/usr/bin/env python


class Callback(object):
    def __init__(self, match, function, args, kwargs):
        self.match = match
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def check_call(self, event):
        if self.match(event):
            self.function(event, *self.args, **self.kwargs)

    def __call__(self, event):
        self.check_call(event)


class Callbacker(object):
    def __init__(self, key=None):
        self.callbacks = {}
        if key is None:
            key = lambda e: e['name']
        self.key = key
        self._next_id = 0
        self._by_id = {}

    def add_callback(self, key, *args, **kwargs):
        """
        Can be called multiple ways.
        All ways must provide the callback key as the first argument
        and can provide other options in either args or kwargs.
        These options are:
            1) callback function or Callback (see Callback object)
            2) match function (see Callback object)
            3) callback args (see Callback object)
            4) callback kwargs (see Callback object)

        add_callback('a', foo)  # where foo is a callable function
        add_callback('a', foo, lambda e: e['bar'] == 2)
        add_callback('a', foo, (1, 2), {'a': 'b'})
        add_callback('a', foo, lambda e: e['bar'] == 2, (1, 2), {'a': 'b'})
        add_callback('a', foocb)  # where foo is a Callback

        keyword arguments can also be used (and will be overwritten by args)

        add_callback('a', foo, args=(1, 2), kwargs={'a': 'b'})
        add_callback('a', foo, match=lambda e: e['bar'] == 2)
        """
        function = kwargs.get('function', None)
        match = kwargs.get('match', None)
        cbargs = kwargs.get('args', None)
        cbkwargs = kwargs.get('kwargs', None)
        if len(args) > 4:
            raise ValueError("Invalid # of args len([%s]) > 4" % args)
        if len(args) == 1:
            function = args[0]
        elif len(args) == 2:
            function, match = args
        elif len(args) == 3:
            function, cbargs, cbkwargs = args
        elif len(args) == 4:
            function, match, cbargs, cbkwargs = args
        if function is None:
            raise ValueError("callback function not defined")
        if isinstance(function, Callback):
            for item in (match, cbargs, cbkwargs):
                if item is not None:
                    raise ValueError("over defined callback [%s is not None]"
                                     % item)
            cb = function
        else:
            if not callable(function):
                raise ValueError("callback function [%s] is not callable"
                                 % function)
            if match is None:
                match = lambda e: True
            cbargs = () if cbargs is None else tuple(cbargs)
            cbkwargs = {} if cbkwargs is None else cbkwargs
            if not callable(match):
                raise ValueError("match must be callable [%s]" % match)
            if not isinstance(cbkwargs, dict):
                raise ValueError("kwargs must be a dict [%s]" % cbkwargs)
            if not isinstance(cbargs, tuple):
                raise ValueError("args must be a tuple [%s]" % cbargs)
            cb = Callback(match, function, cbargs, cbkwargs)
        if key not in self.callbacks:
            self.callbacks[key] = []
        self.callbacks[key].append(cb)
        # this is for removal
        i = self._next_id
        self._next_id += 1
        cb.key = key
        self._by_id[i] = cb
        return i

    def remove_callback(self, i):
        if isinstance(i, (str, unicode)):
            # remove all for a given key
            cbs = self.callbacks[i]
            cids = []
            for cid in self._by_id:
                if self._by_id[cid] in cbs:
                    cids.append(cid)
            for cid in cids:
                self.remove_callback(cid)
        elif isinstance(i, int):
            cb = self._by_id[i]
            self.callbacks[cb.key].remove(cb)
            del self._by_id[i]
        else:
            raise ValueError("Invalid index [%s] should be int or str" % i)

    def process_callbacks(self, event):
        for cb in self.callbacks.get(self.key(event), ()):
            cb(event)


def test():
    cb = Callbacker()
    de = {'name': '0', 'filter': True, 'filterb': True}

    def p(e, *args, **kwargs):
        print '  ', e, args, kwargs

    def m(i):
        print "should print %i events" % i

    def t(cb, **kwargs):
        if kwargs is None:
            kwargs = de
        kwargs['name'] = kwargs.get('name', '0')
        cb.process_callbacks(kwargs)

    # func cb
    cb.add_callback('0', p)
    m(1)
    t(cb)

    # w/match
    cb.add_callback('0', p, lambda e: e.get('filter', False))
    m(1)
    t(cb)
    m(2)
    t(cb, filter=True)

    # w/args
    cb.add_callback('0', p, (1, 2), None)
    m(2)
    t(cb)

    # w/kwargs
    cb.add_callback('0', p, None, {'a': 'b'})
    m(3)
    t(cb)
    cb.add_callback('0', p, lambda e: e.get('filterb', False),
                    (1, 2), {'a': 'b'})
    m(3)
    t(cb)
    m(4)
    t(cb, filter=True)
    m(4)
    t(cb, filterb=True)

    # kwarg/arg add
    cid = cb.add_callback('0', function=p,
                          match=lambda e: e.get('filter', False),
                          args=(1, 2), kwargs={'a': 'b'})
    m(3)
    t(cb)
    m(5)
    t(cb, filter=True)

    # removal
    cb.remove_callback(cid)
    m(3)
    t(cb)
    m(4)
    t(cb, filter=True)

    cb.remove_callback('0')
    m(0)
    t(cb)

    # test non-matching
    m(0)
    t(cb, name='1')

    # TODO incorrect args


if __name__ == '__main__':
    test()
