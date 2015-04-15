from proclib.pipe import Pipe
from proclib.helpers import convert_args


__all__ = ('spawn',)


def spawn(cmds, data=None, hooks=None, env=None, cwd=None):
    pipe = Pipe(commands=list(convert_args(cmds)),
                data=data,
                hooks=hooks,
                env=env,
                cwd=cwd)
    return pipe.run()
