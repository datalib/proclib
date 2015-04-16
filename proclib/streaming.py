"""
    proclib.streaming
    ~~~~~~~~~~~~~~~~~

    Implements streaming alternatives to the standard
    Process, Response, and Pipe interfaces.
"""


from subprocess import PIPE
from .response import Response
from .process import Process
from .pipe import Pipe


class StreamResponse(Response):
    """
    Implements the streaming alternative of the
    Response object. For a StreamResponse, the
    wrapped Popen object needn't complete.
    """

    def setup(self):
        pass

    def wait(self):
        """
        Wait for the response to complete.
        """
        self.process.wait()

    def terminate(self):
        """
        Terminate the process if possible (if
        the process hasn't already been killed
        or exited).
        """
        if not self.finished:
            self.process.terminate()

    @property
    def finished(self):
        """
        Returns a boolean telling if the process
        has completed (exited, killed, etc).
        """
        return self.returncode is not None

    @property
    def pid(self):
        return self.process.pid

    @property
    def returncode(self):
        return self.process.poll()

    def __enter__(self):
        """
        When used as a context manager, the
        StreamingResponse object yields the
        response to the caller for convenience.
        When the block exits, wait for the process
        to exit and then close the stdout and
        stderr file objects.
        """
        return self

    def __exit__(self, *_):
        self.wait()
        self.stdout.close()
        self.stderr.close()


class StreamProcess(Process):
    """
    Streaming variant of Process, the main
    difference is that it doesn't ``communicate``
    with the Popen instance as that will result
    in reading the entire stdout at once.
    """

    def run(self):
        return StreamResponse(
            command=self.command,
            process=self.popen,
            stdout=self.popen.stdout,
            stderr=self.popen.stderr,
            )


class StreamPipe(Pipe):
    """
    Streaming variant of Pipe that uses the
    ``StreamProcess`` as the default Process
    class to be used.
    """

    process_class = StreamProcess

    def order(self):
        return self.commands

    def spawn_procs(self):
        procs = []
        last_stdin = self.data
        for cmd in self.order():
            proc = self.process_class(
                cmd,
                stdin=last_stdin,
                stdout=PIPE,
                **self.opts
                )
            last_stdin = proc.popen.stdout
            procs.append(proc)
        return procs

    def run(self):
        r = super(StreamPipe, self).run()
        for item in r.history:
            item.stdout.close()
        return r
