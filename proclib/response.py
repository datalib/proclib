"""
    proclib.response
    ~~~~~~~~~~~~~~~~
    Implements the Response class.
"""

from .helpers import cached_property
from signalsdb.api import explain


class Response(object):
    """
    A Response object represents the result of running
    a process. The parameters supplied are stored and
    available as attributes as well.

    :param command: A command in the form of a list.
    :param process: A `subprocess.Popen` object.
    """

    def __init__(self, command, process):
        self.history = []
        self.command = command
        self.process = process

        self.pid = process.pid
        self.stdout = process.stdout
        self.stderr = process.stderr

    @cached_property
    def out(self):
        """
        Reads the entire stdout of the Popen instance
        and then returns it. Not recommended for long
        running processes.
        """
        with self.stdout:
            return self.stdout.read()

    @cached_property
    def err(self):
        """
        Similar to ``out``, reads the entirety of
        ``stderr``.
        """
        with self.stderr:
            return self.stderr.read()

    @property
    def status_code(self):
        """
        Returns the exit code of the process, None
        if the process hasn't completed.
        """
        return self.process.poll()

    @property
    def finished(self):
        """
        Returns a boolean stating if the process has
        completed or not. Internally this calls
        `status_code` to determine the exit code
        of the process.
        """
        return self.status_code is not None

    def close(self):
        """
        If possible, close the stdout and stderr file
        handles.
        """
        if self.stdout: self.stdout.close()
        if self.stderr: self.stderr.close()

    @property
    def ok(self):
        """
        Returns a boolean depending on whether the
        `returncode` attribute equals zero.
        """
        return self.status_code == 0

    def wait(self):
        """
        Block until the process to complete.
        """
        self.process.wait()

    def terminate(self):
        """
        Terminate the process if it is not finished.
        """
        if not self.finished:
            self.process.terminate()

    def __repr__(self):
        return '<Response [%s]>' % self.command[0]

    def __enter__(self):
        """
        Similar to a file object, will return the
        Response object and then will safely close
        all open file handles when it exits.
        """
        return self

    def __exit__(self, *_):
        self.close()

    def explain(self):
        """
        Explains (provides the name, the description,
        and the default action of) the signal that
        killed the process.
        """
        status = self.status_code
        if status and status < 0:
            return explain(abs(status))
