from subprocess import PIPE
from procs.process import Process


def spawn(cmd, env=None, cwd=None, data=None):
    return Process.from_config(cmd,
                               data=data,
                               env=env,
                               cwd=cwd).run()


def pipe(cmds, env=None, cwd=None, data=None):
    procs = []
    previous_stdin = PIPE

    for cmd in reversed(cmds):
        proc = Process.from_config(cmd, cwd=cwd, env=env,
                                   stdout=previous_stdin)
        procs.append(proc)
        previous_stdin = proc.popen.stdin

    procs.reverse()
    procs[0].data = data
    responses = [proc.run() for proc in procs]

    r = responses.pop()
    r.history = responses
    return r
