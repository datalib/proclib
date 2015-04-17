from pytest import fixture
from proclib.helpers import str_parse, list_parse, cached_property


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


def test_cached_property():
    class Obj(object):
        ctx = []

        @cached_property
        def name(self):
            self.ctx.append(1)
            return self

    obj = Obj()
    assert obj.name is obj
    assert obj.name is obj
    assert obj.ctx == [1]
