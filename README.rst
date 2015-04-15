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
library subprocess module, written in Python, which aims to
simplify the usage of Unix utilities right from Python and help
the developer focus on the commands and not the code which calls
the commands.

Overview
--------

`proclib.api.spawn(cmd)`
    Given a string or list making up commands *cmd*, return
    a Response object which is the result of piping the commands,
    i.e. they are run in *parallel*. The *data* parameter can be
    used to configure the data passed in to the initial process.
    Usage example::

        >>> from proclib.api import spawn
        >>> proc = spawn('cat | grep at', data='at\n')
        >>> proc.ok
        True
        >>> proc.history
        [<Response [cat]>]

Extending
---------

Extending the library can be done via hooking into the library.
You can provide ``hooks`` parameter which contains a mapping of
event-names to lists of callbacks. Currently only two hooks
are supported:

- ``success`` - Called when the process ran successfully,
  i.e. the return code is 0.
- ``error`` - Called otherwise.

The provided callbacks are called with the Process object, a
simple wrapper that prepares and runs a Popen object. Example
of using the hooking API::

    spawn(command, hooks={
        'success': [callback1, callback2],
        'error': [callback3],
    })
