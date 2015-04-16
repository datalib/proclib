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
    :param hooks: Hooks to be passed to every process.
    :param data: Data to be piped in to the first process.
    :param opts: Extra options to be passed to every
        spawned process.
    """

    process_class = Process

    def __init__(self, commands, hooks=None, data=None, **opts):
        self.commands = commands
        self.hooks = hooks or {}
        self.data = data
        self.opts = opts

    def order(self):
        """
        A list of commands which corresponds to the
        order in which the processes are to be spawned.
        """
        return reversed(self.commands)

    def spawn_procs(self):
        """
        Return a list of processes that have had their
        stdout file handles configured the correct order.
        """
        previous_stdin = PIPE
        procs = []
        for cmd in self.order():
            proc = self.process_class(
                command=cmd,
                hooks=self.hooks,
                stdout=previous_stdin,
                **self.opts
                )
            previous_stdin = proc.popen.stdin
            procs.append(proc)
        procs.reverse()
        return procs

    def run(self):
        """
        Runs the processes. Internally this calls the
        ``spawn_procs`` method but converts them into
        responses via their ``run`` method and returns
        a Response object.
        """
        procs = self.spawn_procs()
        procs[0].data = self.data

        history = [p.run() for p in procs]
        r = history.pop()
        r.history = history
        return r
