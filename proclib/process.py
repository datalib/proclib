"""
    proclib.process
    ~~~~~~~~~~~~~~~

    Implements the Process class.
"""

from subprocess import Popen, PIPE
from .response import Response
from .helpers import restore_signals


class Process(object):
    """
    A Process object is a wrapper around a regular
    `subprocess.Popen` instance that knows how to
    call it with the correct arguments.

    :param command: The command.
    :param opts: Keyword argument of additional
        options to be pased to the `subprocess.Popen`
        constructor.
    """

    response_class = Response
    defaults = dict(universal_newlines=True,
                    close_fds=True,
                    preexec_fn=restore_signals,
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE)

    def __init__(self, command, **opts):
        conf = self.defaults.copy()
        conf.update(opts)

        self.command = command
        self.process = Popen(args=command, **conf)

    def pipe(self, lines):
        """
        Given a Process with a valid stdin (not a
        file-handle that is not PIPE), write *lines*
        of data to the process where *lines* can
        be any iterable.

        :param lines: Iterable of data to be piped
            in to the process.
        """
        with self.process.stdin as stdin:
            for line in lines:
                stdin.write(line)
            stdin.flush()

    def run(self):
        """
        Wraps the Popen instance in a ``Response``
        object.
        """
        return self.response_class(
            self.command,
            self.process,
            )
