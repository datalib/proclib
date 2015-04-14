Procs: Pythonic Processes
=========================

Procs is a high level wrapper/abstraction around the standard
library subprocess module, written in Python, which aims to
simplify the usage of Unix utilities right from Python and help
the developer focus on the commands and not the code which calls
the commands.

Overview
--------

`procs.api.spawn(cmd)`
    Given a list of strings or lists making up commands *cmd*,
    return a Response object which is the result of (truly)
    piping the commands. The *data* parameter can be used to
    configure the data passed in to the initial process.
    Usage example::

        >>> from procs.api import spawn
        >>> proc = spawn(['cat', 'grep at'], data='at\n')
        >>> proc.ok
        True
        >>> proc.history
        [<Response [cat]>]

    You can also make 'hooks' for your processes, i.e. functions
    that will be called when certain events occur. Currently
    there are only two hooks available:

     - **on_start**: Ran before running the Popen object.
     - **on_exit**: Ran when the process terminates.

    They will all be called with the ``Process`` object, a
    simple wrapper around a ``Popen`` object. You can add
    hooks by subclassing the ``Handler`` class, for example::

        from procs.pipes import Handler

        class MyHandler(Handler):
            def on_start(self, proc):
                print(proc)

        >>> spawn(['echo hi'], handler=MyHandler())
        <Process [echo hi]>
        <Response [echo]>
