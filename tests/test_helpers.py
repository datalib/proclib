from pytest import fixture
from proclib.helpers import str_parse, list_parse, dispatch_hook


@fixture
def expected():
    return [['cat'], ['grep', 'at']]


@fixture(params=[
    ['cat | grep at'],
    ['cat', 'grep at'],
    ['cat', ['grep', 'at']],
])
def cmd(request):
    return request.param


def test_str_parse(expected):
    assert str_parse('cat | grep at') == expected


def test_list_parse(cmd, expected):
    assert list_parse(cmd) == expected


def test_dispatch_hook_silent_error():
    assert dispatch_hook({}, 's', 1) == 1


def test_dispatch_hook_calls_hooks():
    ctx = []
    assert dispatch_hook({'s': [ctx.append]}, 's', 1) == 1
    assert ctx == [1]
