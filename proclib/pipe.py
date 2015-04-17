from subprocess import PIPE
from .process import Process


class Pipe(object):
    process_class = Process

    def __init__(self, commands, data=None, **opts):
        self.commands = commands
        self.data = data
        self.opts = opts

    def spawn_procs(self):
        stdout = PIPE
        for item in self.commands:
            proc = self.process_class(
                command=item,
                stdin=stdout,
                **self.opts
                )
            stdout = proc.process.stdout
            yield proc

    def run(self):
        procs = list(self.spawn_procs())
        procs[0].pipe(self.data)

        history = [p.run() for p in procs]
        r = history.pop()
        r.history = history
        return r
