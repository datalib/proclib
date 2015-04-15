from contextlib import contextmanager
from subprocess import Popen, PIPE
from proclib.response import Response
from proclib.helpers import dispatch_hook


class Process(object):
    defaults = dict(universal_newlines=True,
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE)

    def __init__(self, command, hooks=None, data=None, **opts):
        conf = self.defaults.copy()
        conf.update(opts)

        self.popen = Popen(args=command, **conf)
        self.command = command
        self.hooks = hooks or {}
        self.data = data

    def dispatch(self, hook):
        dispatch_hook(self.hooks, hook, self)

    @contextmanager
    def popen_context(self):
        yield self.popen
        self.dispatch('error' if self.popen.returncode else
                      'success')

    def run(self):
        with self.popen_context() as popen:
            stdout, stderr = popen.communicate(self.data)
            return Response(
                    command=self.command,
                    process=popen,
                    stdout=stdout,
                    stderr=stderr,
                    returncode=popen.wait(),
                    pid=popen.pid,
                    )

    def __repr__(self):
        return '<Process [%s]>' % ' '.join(self.command)
