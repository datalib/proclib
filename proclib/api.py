"""
    proclib.api
    ~~~~~~~~~~~

    Module that exposes the public, easy-to-use
    functional wrappers.
"""


from .pipe import Pipe
from .helpers import list_parse, str_parse


__all__ = ('spawn',)


def spawn(cmds, data=None, hooks=None, env=None, cwd=None):
    """
    Spawn a command/pipeline *cmds* where *cmds*
    can be a string, list of strings, or list of
    lists.

    :param cmds: List/String of commands.
    :param data: Data to be piped in.
    :param hooks: Hooks to be passed in.
    :param env: Optionally override the environment
        variables of all the commands to be ran.
    :param cwd: Optionally set the execution directory
        of the commands ran.
    """
    func = str_parse if isinstance(cmds, str) else list_parse
    pipe = Pipe(commands=list(func(cmds)),
                hooks=hooks,
                data=data,
                env=env,
                cwd=cwd)
    return pipe.run()
