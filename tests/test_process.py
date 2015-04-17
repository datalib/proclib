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
    assert r.status_code == -15
    assert not r.ok
