from subprocess import Popen, PIPE
from pytest import fixture
from proclib.streaming import StreamProcess, \
        StreamResponse, StreamPipe


@fixture
def response(request):
    p = Popen('cat', stdout=PIPE, stdin=PIPE, stderr=PIPE)
    request.addfinalizer(p.terminate)
    return StreamResponse(['cat'], p, p.stdout, p.stderr)


def test_unfinished_response_returncode(response):
    assert response.returncode is None
    response.process.terminate()
    assert not response.ok


def test_response_contextmanager(response):
    assert not response.stdout.closed
    assert not response.stderr.closed
    with response:
        pass
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
