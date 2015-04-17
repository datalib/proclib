from .helpers import cached_property


class Response(object):
    def __init__(self, command, process):
        self.history = []
        self.command = command
        self.process = process

        self.pid = process.pid
        self.stdout = process.stdout
        self.stderr = process.stderr

    @cached_property
    def out(self):
        with self.stdout:
            return self.stdout.read()

    @cached_property
    def err(self):
        with self.stderr:
            return self.stderr.read()

    @property
    def status_code(self):
        return self.process.poll()

    @property
    def finished(self):
        return self.status_code is not None

    def close(self):
        self.stdout.close()
        self.stderr.close()

    @property
    def ok(self):
        return self.status_code == 0

    def wait(self):
        self.process.wait()
