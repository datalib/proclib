from subprocess import PIPE
from procs.process import Process


class Pipe(object):
    def __init__(self, commands, data, **opts):
        self.commands = commands
        self.data = data
        self.opts = opts

    def order(self):
        return reversed(self.commands)

    def spawn(self, cmd, stdout=PIPE):
        return Process(
                command=cmd,
                stdin=PIPE,
                stdout=stdout,
                stderr=PIPE,
                universal_newlines=True,
                **self.opts
                )

    def spawn_procs(self):
        previous_stdin = PIPE
        procs = []
        for cmd in self.order():
            proc = self.spawn(cmd, previous_stdin)
            previous_stdin = proc.popen.stdin
            procs.append(proc)
        procs.reverse()
        return procs

    def run(self):
        procs = self.spawn_procs()
        procs[0].data = self.data

        history = [p.run() for p in procs]
        r = history.pop()
        r.history = history
        return r
