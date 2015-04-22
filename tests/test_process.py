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

    assert r.finished
    assert r.explain()['signal'] == 'SIGTERM'
    assert not r.ok


def test_context_manager(proc):
    proc.pipe(['data'])
    with proc.run() as r:
        assert r.stdout.read() == 'data'
        assert r.stderr.read() == ''

    assert r.stdout.closed
    assert r.stderr.closed
    r.wait()
