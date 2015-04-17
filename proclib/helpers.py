import shlex


def str_parse(cmds):
    buff = []
    for item in shlex.split(cmds):
        if item == '|':
            yield buff
            buff = []
            continue
        buff.append(item)

    if buff:
        yield buff


def list_parse(cmds):
    for item in cmds:
        if isinstance(item, str):
            for item in str_parse(item):
                yield item
            continue
        yield list(item)


class cached_property(object):
    def __init__(self, func):
        self.__doc__ = func.__doc__
        self.getter = func
        self.attr = func.__name__

    def __get__(self, obj, objtype=None):
        if obj is not None:
            value = self.getter(obj)
            self.getter = lambda _: value
            return value
        return self
