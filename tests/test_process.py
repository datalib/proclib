from pytest import fixture
from proclib.process import Process


@fixture
def proc():
    return Process('cat', data='at\n')


def test_run_calls_command(proc):
    r = proc.run()
    assert r.ok
    assert r.stdout == 'at\n'
    assert not r.stderr
    assert not r.history
