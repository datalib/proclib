from subprocess import Popen, PIPE
from procs.response import Response


class Process(object):
    defaults = dict(universal_newlines=True,
                    stdout=PIPE, stdin=PIPE,
                    stderr=PIPE)

    def __init__(self, command, data=None, **opts):
        options = self.defaults.copy()
        options.update(opts)
        self.popen = Popen(args=command, **options)
        self.command = command
        self.data = data

    def run(self):
        stdout, stderr = self.popen.communicate(self.data)
        status = self.popen.wait()
        return Response(
                command=self.command,
                process=self,
                stdout=stdout,
                stderr=stderr,
                returncode=status,
                pid=self.popen.pid,
                )

    def __repr__(self):
        return '<Process [%s]>' % ' '.join(self.command)
