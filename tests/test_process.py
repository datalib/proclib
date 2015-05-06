import warnings
from contextlib import closing
from pytest import fixture
from proclib.process import Process


@fixture
def proc():
    return Process('cat')


def test_pipe_passes_data(proc):
    proc.pipe(['at'])
    r = proc.run()
    r.wait()

    with closing(r):
        assert r.out == 'at'
        assert r.err == ''
        assert r.ok
        assert r.pid


def test_terminate_cat(proc):
    r = proc.run()
    r.terminate()
    r.wait()

    sig = r.explain_signal()
    assert r.finished
    assert sig['signal'] == 'SIGTERM'
    assert sig['id'] == 15
    assert not r.ok


def test_context_manager(proc):
    proc.pipe(['data'])
    with proc.run() as r:
        assert r.stdout.read() == 'data'
        assert r.stderr.read() == ''

    assert r.stdout.closed
    assert r.stderr.closed
    r.wait()


def test_iter(proc):
    proc.pipe(['data\ndata\ndata\n'])
    with proc.run() as r:
        assert list(r) == (['data\n'] * 3)
        assert not r.stdout.closed


def test_explain_warning(proc):
    r = proc.run()
    r.terminate()
    r.wait()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        r.explain()
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
