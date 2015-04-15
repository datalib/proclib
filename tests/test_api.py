from pytest import mark
from procs.api import spawn


@mark.parametrize('cmd', (
    'echo hello',
    [['echo', 'hello']],
    ['echo hello'],
))
def test_spawn_parses_all_argtypes(cmd):
    assert spawn(cmd).stdout == 'hello\n'
