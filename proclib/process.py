from subprocess import Popen, PIPE
from .response import Response


class Process(object):
    response_cls = Response
    defaults = dict(universal_newlines=True,
                    close_fds=False,
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE)

    def __init__(self, command, **opts):
        conf = self.defaults.copy()
        conf.update(opts)

        self.command = command
        self.process = Popen(args=command, **conf)

    def pipe(self, lines):
        stdin = self.process.stdin
        if stdin:
            for line in lines:
                stdin.write(line)
            stdin.flush()
            stdin.close()

    def run(self):
        return self.response_cls(
            self.command,
            self.process,
            )
