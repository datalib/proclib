from subprocess import Popen, PIPE
from pytest import fixture
from proclib.streaming import StreamProcess, \
        StreamResponse, StreamPipe


@fixture
def response(request):
    p = Popen(['echo', 'm'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    res = StreamResponse(['echo', 'm'], p, p.stdout, p.stderr)
    request.addfinalizer(res.terminate)
    return res


def test_response_returncode(response):
    assert response.ok


def test_response_contextmanager(response):
    with response:
        assert response.stdout.read() == 'm\n'
        assert not response.stderr.read()
    assert response.stdout.closed
    assert response.stderr.closed


@fixture
def process(request):
    return StreamProcess(['echo', 'm'])


def test_process_run(process):
    res = process.run()
    with res:
        assert res.stdout.read() == 'm\n'
    assert res.ok


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
