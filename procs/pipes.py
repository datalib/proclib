from subprocess import PIPE
from procs.process import ProcessSpawner, Process


class Pipe(object):
    def __init__(self, commands, data=None, **opts):
        self.commands = commands
        self.order = reversed(commands)
        self.data = data
        self.opts = opts

    def spawn(self):
        spawners = []
        stdout = PIPE

        for item in self.order:
            spawner = ProcessSpawner(item, stdout=stdout, **self.opts)
            spawners.append(spawner)
            stdout = spawner.popen.stdout

        spawners = reversed(spawners)
        last = spawners[-1]
        last.data = self.data

        history = [s.spawn() for s in spawners]
        r = history.pop()
        r.history = history
        return r
