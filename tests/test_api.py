import pytest
try:
    from cStringIO import StringIO
except:
    from io import StringIO
from proclib.api import spawn


@pytest.fixture(params=[
    ['cat', ['grep', 'at']],
    ['cat | grep at'],
    'cat | grep at',
])
def command(request):
    return request.param


@pytest.fixture(params=[
    lambda: iter(['at\n'] * 2),
    lambda: 'at\nat\n',
    lambda: ['at\nat\n'],
    lambda: StringIO('at\nat\n'),
])
def data(request):
    return request.param()


def test_spawn_no_data():
    r = spawn('echo m')
    r.wait()

    assert r.out.strip() == 'm'
    assert r.ok


def test_spawn_with_data(command, data):
    r = spawn(command, data=data)
    r.wait()

    assert r.out == 'at\nat\n'
    assert r.ok
