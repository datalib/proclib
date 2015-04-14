import shlex
from subprocess import PIPE
from procs.process import Process


def convert_args(cmds):
    for item in cmds:
        if isinstance(item, str):
            yield shlex.split(item)
            continue
        yield item


def spawn(cmds, env=None, cwd=None, data=None):
    cmds = list(convert_args(cmds))
    procs = []
    previous_stdin = PIPE

    for cmd in reversed(cmds):
        proc = Process(cmd, cwd=cwd, env=env, stdout=previous_stdin)
        procs.append(proc)
        previous_stdin = proc.popen.stdin

    procs.reverse()
    procs[0].data = data
    responses = [proc.run() for proc in procs]

    r = responses.pop()
    r.history = responses
    return r
