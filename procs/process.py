from subprocess import Popen, PIPE
from procs.response import Response


class Process(object):
    def __init__(self, command, data=None, **opts):
        self.popen = Popen(args=command, **opts)
        self.command = command
        self.data = data

    def run(self):
        stdout, stderr = self.popen.communicate(self.data)
        status = self.popen.wait()
        return Response(
                command=self.command,
                process=self.popen,
                stdout=stdout,
                stderr=stderr,
                returncode=status,
                pid=self.popen.pid,
                )

    def __repr__(self):
        return '<Process [%s]>' % ' '.join(self.command)
