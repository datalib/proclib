.. image:: https://raw.githubusercontent.com/datalib/proclib/master/media/logo-small.png

Proclib is a high level wrapper/abstraction around the standard
library subprocess module, written in Python, with proper piping
support which aims to simplify the usage of Unix utilities right
from Python and help the developer focus on the commands and not
the code which calls the commands.

.. image:: https://travis-ci.org/datalib/proclib.svg?branch=master
    :target: https://travis-ci.org/datalib/proclib

Overview
--------

`proclib.api.spawn(cmd)`
    Given a string or list making up commands *cmd*, return
    a Response object which is the result of piping the commands,
    i.e. they are run in *parallel*. The ``data`` parameter can be
    used to configure the data passed in to the initial process.
    Usage example::

        >>> from proclib.api import spawn
        >>> r = spawn('yes | head')
        >>> r.stdout.read()
        'y\ny\ny\ny\ny\ny\ny\ny\ny\ny\n'
        >>> r.close()
        >>> r.history[0].explain_signal()
        {'action': 'kill',
         'description': 'write on a pipe with no readers',
         'id': 13,
         'signal': 'SIGPIPE'}

    Streaming support is built-in- that is that the stdout of
    any process can be streamed lazily instead of read and stored
    in memory all in one go. Also, any kind of iterable can be
    piped to the process::

        def gen():
            yield 'hi\n'
            yield 'ho\n'

        r = spawn('cat', data=gen())
        assert r.out.split() == ['hi', 'ho']
