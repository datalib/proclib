class Response(object):
    def __init__(self, command, process, stdout,
            stderr, returncode, pid):
        self.history = []
        self.command = command
        self.process = process
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.pid = pid

    @property
    def ok(self):
        return self.returncode == 0
