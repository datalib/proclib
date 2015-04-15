from procs.pipes import Pipe
from procs.parse_helpers import convert_args


__all__ = ('spawn',)


def spawn(cmds, data=None, env=None, cwd=None):
    pipe = Pipe(commands=list(convert_args(cmds)),
                data=data,
                env=env,
                cwd=cwd)
    return pipe.run()
