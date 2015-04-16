from subprocess import Popen, PIPE
from pytest import fixture
from proclib.streaming import StreamProcess, \
        StreamResponse, StreamPipe


@fixture
def response(request):
    p = Popen('cat', stdout=PIPE, stdin=PIPE, stderr=PIPE)
    request.addfinalizer(p.terminate)
    return StreamResponse('cat', p, p.stdout, p.stderr)


def test_unfinished_response_returncode(response):
    assert response.returncode is None
    response.process.terminate()
    assert response.returncode < 0


def test_response_contextmanager(response):
    assert not response.stdout.closed
    assert not response.stderr.closed
    with response:
        pass
    assert response.stdout.closed
    assert response.stderr.closed
