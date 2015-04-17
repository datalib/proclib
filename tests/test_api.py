import pytest
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
])
def data(request):
    return request.param()


def test_spawn(command, data):
    r = spawn(command, data=data)
    r.wait()

    assert r.out == 'at\nat\n'
    assert r.ok
