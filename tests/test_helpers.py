from pytest import fixture
from proclib.helpers import str_parse, list_parse


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
    assert list(str_parse('cat | grep at')) == expected


def test_list_parse(cmd, expected):
    assert list(list_parse(cmd)) == expected
