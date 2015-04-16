Proclib: pythonic processes
===========================

.. image:: https://travis-ci.org/datalib/proclib.svg?branch=master
    :target: https://travis-ci.org/datalib/proclib

::

                          ___ __
       ___  _______  ____/ (_) /
      / _ \/ __/ _ \/ __/ / / _ \
     / .__/_/  \___/\__/_/_/_.__/
    /_/


Proclib is a high level wrapper/abstraction around the standard
library subprocess module, written in Python, with proper piping
support which aims to simplify the usage of Unix utilities right
from Python and help the developer focus on the commands and not
the code which calls the commands.

Overview
--------

`proclib.api.spawn(cmd)`
    Given a string or list making up commands *cmd*, return
    a Response object which is the result of piping the commands,
    i.e. they are run in *parallel*. The ``data`` parameter can be
    used to configure the data passed in to the initial process.
    Usage example::

        >>> from proclib.api import spawn
        >>> r = spawn('cat | grep at', data='at\n')
        >>> r.ok
        True
        >>> r.history
        [<Response [cat]>]

`proclib.api.stream(cmd)`
    Given a string or list of commands *cmd*, returns the
    streaming variant of a Response object, StreamResponse
    which encapsulates a long running, possibly unfinished
    process. The ``fileobj`` parameter can be used to supply
    a file as the stdin. Usage example::

        >>> from proclib.api import stream
        >>> r = stream('cat', fileobj=open('lorem.txt'))
        >>> for item in r.stdout: print(item)
        Lorem ipsum dolor sit amet, cras rutrum a, vivamus
        placerat amet vehicula rhoncus interdum, semper in
        ...
