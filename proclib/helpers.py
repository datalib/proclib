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
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        res = obj.__dict__[self.__name__] = self.func(obj)
        return res
