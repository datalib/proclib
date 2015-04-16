"""
    proclib.api
    ~~~~~~~~~~~

    Module that exposes the public, easy-to-use
    functional wrappers.
"""


from subprocess import PIPE
from .helpers import list_parse, str_parse
from .pipe import Pipe
from .streaming import StreamPipe


__all__ = ('spawn',)


def parse(cmds):
    parser = str_parse if isinstance(cmds, str) else list_parse
    return list(parser(cmds))


def spawn(cmds, data=None, env=None, cwd=None):
    """
    Spawn a command/pipeline *cmds* where *cmds*
    can be a string, list of strings, or list of
    lists.

    :param cmds: List/String of commands.
    :param data: Data to be piped in.
    :param env: Optionally override the environment
        variables of all the commands to be ran.
    :param cwd: Optionally set the execution directory
        of the commands ran.
    """
    pipe = Pipe(commands=parse(cmds),
                data=data,
                env=env,
                cwd=cwd)
    return pipe.run()


def stream(cmds, fileobj=PIPE, env=None, cwd=None):
    pipe = StreamPipe(commands=parse(cmds),
                      data=fileobj,
                      env=env,
                      cwd=cwd)
    return pipe.run()
