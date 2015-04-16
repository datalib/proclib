"""
    proclib.process
    ~~~~~~~~~~~~~~~

    Implements the Process class.
"""


from contextlib import contextmanager
from subprocess import Popen, PIPE
from .response import Response
from .helpers import dispatch_hook


class Process(object):
    """
    A Process object is a wrapper around a regular
    `subprocess.Popen` instance that knows how to
    call and manipulate it with the correct
    arguments.

    :param command: The command.
    :param hooks: A dictionary of hooks.
    :param data: Data to be piped in to the process.
    :param opts: Keyword argument of additional
        options to be pased to the `subprocess.Popen`
        constructor.
    """

    defaults = dict(universal_newlines=True,
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE)

    def __init__(self, command, hooks=None, data=None, **opts):
        conf = self.defaults.copy()
        conf.update(opts)

        self.popen = Popen(args=command, **conf)
        self.command = command
        self.hooks = hooks or {}
        self.data = data

    def dispatch(self, hook):
        """
        Runs a given *hook*.
        """
        dispatch_hook(self.hooks, hook, self)

    @contextmanager
    def popen_context(self):
        """
        A context manager that yields the internal
        Popen object and runs the ``error`` or
        ``success`` hook depending on the exit code.
        """
        yield self.popen
        self.dispatch('error' if self.popen.returncode else
                      'success')

    def run(self):
        """
        Communicates with the Popen object and then
        waits for it to exit. Triggers hooks and
        returns a ``Response`` object.
        """
        with self.popen_context() as popen:
            stdout, stderr = popen.communicate(self.data)
            return Response(
                    command=self.command,
                    process=popen,
                    stdout=stdout,
                    stderr=stderr,
                    returncode=popen.wait(),
                    pid=popen.pid,
                    )

    def __repr__(self):
        return '<Process [%s]>' % ' '.join(self.command)
