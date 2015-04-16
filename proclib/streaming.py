from subprocess import PIPE
from .response import Response
from .process import Process
from .pipe import Pipe


class StreamResponse(Response):
    def __init__(self, command, process, stdout, stderr):
        self.history = []
        self.command = command
        self.process = process
        self.stdout = stdout
        self.stderr = stderr

    @property
    def pid(self):
        if self.returncode is not None:
            return self.process.pid
        return None

    @property
    def returncode(self):
        self.process.poll()
        return self.process.returncode

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.stdout.close()
        self.stderr.close()


class StreamProcess(Process):
    def run(self):
        return StreamResponse(
                command=self.command,
                process=self.popen,
                stdout=self.popen.stdout,
                stderr=self.popen.stderr,
                )


class StreamPipe(Pipe):
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
