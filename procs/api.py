import shlex
from procs.pipes import Pipe


__all__ = ('spawn',)


def convert_args(cmds):
    for item in cmds:
        if isinstance(item, str):
            yield shlex.split(item)
            continue
        yield item


def spawn(cmds, data=None, env=None, cwd=None):
    pipe = Pipe(commands=list(convert_args(cmds)),
                data=data,
                env=env,
                cwd=cwd)
    return pipe.run()
