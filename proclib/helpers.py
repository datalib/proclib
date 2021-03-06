"""
    proclib.helpers
    ~~~~~~~~~~~~~~~

    Helper utility functions.
"""

import shlex
import signal


TO_RESTORE = tuple(
    getattr(signal, sig) for sig in ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ')
    if hasattr(signal, sig)
    )


def restore_signals(signals=TO_RESTORE):
    """
    Restores signals before the process is
    executed so that they can be terminated
    with SIGPIPE.

    :param signals: Optimization detail
        that defaults to integers corresponding
        to SIGPIPE, SIGXFZ, and SIGXFSZ (if
        they are available).
    """
    for sig in signals:
        signal.signal(sig, signal.SIG_DFL)


def str_parse(cmds, pipe_operator='|'):
    """
    Given a string of commands *cmds* yield the
    command in chunks, separated by the *pipe_operator*
    defaulting to '|'.

    :param cmds: String of commands.
    :param pipe_operator: The pipe operator.
    """
    buff = []
    for item in shlex.split(cmds):
        if item == pipe_operator:
            yield buff
            buff = []
            continue
        buff.append(item)
    if buff:
        yield buff


def list_parse(cmds):
    """
    Given a list of commands, if they are a
    string then parse them, else yield them
    as if they were already correctly formatted.

    :param cmds: List of commands.
    """
    for item in cmds:
        if isinstance(item, str):
            for item in str_parse(item):
                yield item
            continue
        yield list(item)


class cached_property(object):
    """
    Property that is computed only once during
    the lifetime of an object, i.e. the second
    time the attribute is looked up there is
    zero cost overhead.

    :param func: Function to wrap over.
    """

    def __init__(self, func):
        self.getter = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, objtype=None):
        if instance is None:
            return self
        res = instance.__dict__[self.__name__] = self.getter(instance)
        return res
