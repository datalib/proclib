from subprocess import PIPE
from proclib.process import Process


class Pipe(object):
    process_class = Process

    def __init__(self, commands, data, hooks=None, **opts):
        self.commands = commands
        self.hooks = hooks or {}
        self.data = data
        self.opts = opts

    def order(self):
        return reversed(self.commands)

    def make_process(self, cmd, stdout=PIPE):
        return self.process_class(
                command=cmd,
                hooks=self.hooks,
                stdout=stdout,
                **self.opts
                )

    def spawn_procs(self):
        previous_stdin = PIPE
        procs = []
        for cmd in self.order():
            proc = self.make_process(cmd, previous_stdin)
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
