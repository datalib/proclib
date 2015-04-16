from subprocess import PIPE
from .response import Response
from .process import Process
from .pipe import Pipe


class StreamResponse(Response):
    def setup(self):
        pass

    @property
    def pid(self):
        return self.process.pid

    def wait(self):
        self.process.wait()

    def terminate(self):
        if not self.finished:
            self.process.terminate()

    @property
    def finished(self):
        return self.returncode is not None

    @property
    def returncode(self):
        return self.process.poll()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.wait()
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
