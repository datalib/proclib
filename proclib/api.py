"""
    proclib.api
    ~~~~~~~~~~~
    Module that exposes the public, easy-to-use
    functional wrappers.
"""

from .helpers import str_parse, list_parse
from .pipe import Pipe

__all__ = ('spawn',)


def parse(cmds):
    """
    Given a string or list of lists/strings *cmds*,
    determine and use the correct parser to use and
    return the results as a list.
    :param cmds: List/String of commands.
    """
    parser = str_parse if isinstance(cmds, str) else list_parse
    return list(parser(cmds))


def spawn(cmd, data=(), env=None, cwd=None):
    """
    Given a string or list making up commands *cmd*,
    return a response object which is the result of
    piping the commands in parallel. Optionally, pass
    in some *data* in the form of an iterable, file
    object, or string to the first process.

    :param cmd: String/List of commands.
    :param data: Data to be passed to the first command.
    :param env: Override environment variables.
    :param cwd: Override working directory.
    """
    if isinstance(data, str):
        data = [data]

    pipe = Pipe(
        commands=parse(cmd),
        data=data,
        env=env,
        cwd=cwd,
        )
    return pipe.run()
