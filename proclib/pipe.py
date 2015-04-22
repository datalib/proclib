"""
    proclib.pipe
    ~~~~~~~~~~~~

    Implements the Pipe object.
"""

from subprocess import PIPE
from .process import Process


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

    @staticmethod
    def make_response(procs):
        """
        Given an iterable of processes *procs*, run all of
        them and pop the last one, returning it as the
        result of running all of them in a pipe.

        :param procs: An iterable of processes.
        """
        history = [p.run() for p in procs]
        r = history.pop()
        r.history = history

        for res in r.history:
            res.stdout.close()

        return r

    def run(self):
        """
        Runs the processes. Internally this calls the
        ``spawn_procs`` method but converts them into
        responses via their ``run`` method and the
        ``make_response`` method.
        """
        procs = list(self.spawn_procs())
        procs[0].pipe(self.data)
        return self.make_response(procs)
