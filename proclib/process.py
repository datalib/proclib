"""
    proclib.process
    ~~~~~~~~~~~~~~~

    Implements the Process class.
"""


from subprocess import Popen, PIPE
from .response import Response


class Process(object):
    """
    A Process object is a wrapper around a regular
    `subprocess.Popen` instance that knows how to
    call and manipulate it with the correct
    arguments.

    :param command: The command.
    :param data: Data to be piped in to the process.
    :param opts: Keyword argument of additional
        options to be pased to the `subprocess.Popen`
        constructor.
    """

    defaults = dict(universal_newlines=True,
                    close_fds=True,
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE)

    def __init__(self, command, data=None, **opts):
        conf = self.defaults.copy()
        conf.update(opts)

        self.popen = Popen(args=command, **conf)
        self.command = command
        self.data = data

    def run(self):
        """
        Communicates with the Popen object and then
        waits for it to exit. Returns a ``Response``
        object.
        """
        stdout, stderr = self.popen.communicate(self.data)
        self.popen.wait()
        return Response(
            command=self.command,
            process=self.popen,
            stdout=stdout,
            stderr=stderr,
            )

    def __repr__(self):
        return '<Process [%s]>' % ' '.join(self.command)
