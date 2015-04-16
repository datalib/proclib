from pytest import fixture
from proclib.streaming import StreamProcess, StreamPipe


@fixture
def res():
    return StreamProcess(['cat']).run()


def test_response_peaceful(res):
    _, _ = res.process.communicate('hello')
    assert res.finished
    assert res.ok


def test_response_killed(res):
    res.terminate()
    res.wait()

    assert res.finished
    assert not res.ok


def test_response():
    r = StreamProcess(['echo', 'm']).run()
    with r:
        assert r.stdout.read() == 'm\n'
        assert not r.stderr.read()

    assert r.finished
    assert r.stdout.closed
    assert r.stderr.closed
    assert r.ok


@fixture
def pipe(request):
    return StreamPipe([['yes'], ['cat'], ['head', '-n', '5']])


def test_pipe_run(pipe):
    r = pipe.run()
    with r:
        assert r.command[0] == 'head'
        assert r.stdout.read() == 'y\ny\ny\ny\ny\n'

    [p.terminate() for p in r.history]
    assert r.returncode == 0
