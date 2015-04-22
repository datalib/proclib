"""
    proclib.pipe
    ~~~~~~~~~~~~

    Implements the Pipe object.
"""

from subprocess import PIPE
from .process import Process


def make_response(procs):
    history = [p.run() for p in procs]
    r = history.pop()
    r.history = history

    for res in r.history:
        res.stdout.close()

    return r


class Pipe(object):
    """
    A Pipe object represents and starts the parallel
    execution and piping of multiple Processes.

    :param commands: A list of commands.
    :param data: Data to be piped in to the first process.
    :param opts: Extra options to be passed to every
        spawned process.
    """

    process_class = Process

    def __init__(self, commands, data=(), **opts):
        self.commands = commands
        self.data = data
        self.opts = opts

    def spawn_procs(self):
        """
        Return a list of processes that have had their
        file handles configured the correct order.
        """
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
        """
        Runs the processes. Internally this calls the
        ``spawn_procs`` method but converts them into
        responses via their ``run`` method and returns
        a Response object. This also closes the stdout
        file handles of all but the last response.
        """
        procs = list(self.spawn_procs())
        procs[0].pipe(self.data)
        return make_response(procs)
