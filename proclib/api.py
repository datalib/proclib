from .helpers import str_parse, list_parse
from .pipe import Pipe


def spawn(cmd, data=None, env=None, cwd=None):
    if isinstance(data, str):
        data = [data]

    func = str_parse if isinstance(cmd, str) else list_parse
    pipe = Pipe(
        commands=list(func(cmd)),
        data=data,
        env=env,
        cwd=cwd,
        )
    return pipe.run()
