Procs: Pythonic Processes
=========================

Procs is a Pythonic library for creating and managing
processes, and a simple, intuitive, and extensible
wrapper around the subprocess library. Usage example:

.. code-block:: python

    >>> from procs.api import spawn
    >>> proc = spawn(['cat', 'grep at'], data='at\n')
    >>> proc.ok
    True
    >>> proc.history
    [<Response [cat]>]
