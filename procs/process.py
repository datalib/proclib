from subprocess import Popen, PIPE
from procs.response import Response


class Process(object):
    defaults = dict(universal_newlines=True,
                    stdout=PIPE, stdin=PIPE,
                    stderr=PIPE)

    def __init__(self, command, data, popen):
        self.command = command
        self.data = data
        self.popen = popen

    def run(self):
        stdout, stderr = self.popen.communicate(self.data)
        status = self.popen.wait()
        return Response(
                command=self.command,
                process=self,
                stdout=stdout,
                stderr=stderr,
                returncode=status,
                pid=self.popen.pid)

    def __repr__(self):
        return '<Process [%s]>' % ' '.join(self.command)

    @classmethod
    def from_config(cls, command, data=None, **opts):
        conf = cls.defaults.copy()
        conf['args'] = command
        conf.update(opts)
        return Process(command,
                       data,
                       Popen(**conf))
