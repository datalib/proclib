from pytest import fixture
from proclib.streaming import StreamProcess, StreamPipe


@fixture
def response(request):
    return StreamProcess(['echo', 'm']).run()


def test_response(response):
    with response:
        assert response.stdout.read() == 'm\n'
        assert not response.stderr.read()
    assert response.stdout.closed
    assert response.stderr.closed
    assert response.ok


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
