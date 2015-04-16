from pytest import fixture
from collections import namedtuple
from proclib.response import Response


Proc = namedtuple('Proc', ('pid', 'returncode'))


@fixture
def res():
    return Response(
        command=['command'],
        process=Proc(100, 1),
        stdout='a',
        stderr='b',
        )


def test_response_attrs(res):
    assert res.pid == 100
    assert res.returncode == 1
    assert res.stdout == 'a'
    assert res.stderr == 'b'


def test_response_ok_when_zero(res):
    assert not res.ok


def test_response_not_ok_when_zero(res):
    res.returncode = 0
    assert res.ok
