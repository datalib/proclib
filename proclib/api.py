from proclib.pipe import Pipe
from proclib.helpers import list_parse, str_parse


__all__ = ('spawn',)


def spawn(cmds, data=None, hooks=None, env=None, cwd=None):
    func = str_parse if isinstance(cmds, str) else list_parse
    pipe = Pipe(commands=func(cmds),
                data=data,
                hooks=hooks,
                env=env,
                cwd=cwd)
    return pipe.run()
