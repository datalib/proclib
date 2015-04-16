from pytest import mark
from proclib.api import spawn, stream


@mark.parametrize('cmd', (
    'echo hello | cat',
    [['echo', 'hello'], 'cat'],
    ['echo hello', 'cat'],
    ['echo hello | cat'],
))
def test_spawn_parses_all_argtypes(cmd):
    assert spawn(cmd).stdout == 'hello\n'



def test_stream_with_fileobj(tmpdir):
    u = tmpdir.join('filename.txt')
    u.write('\n'.join(['ho'] * 10))

    with u.open() as fp:
        with stream('cat | head -n 2', fileobj=fp) as res:
            res.wait()
            assert res.stdout.read() == 'ho\nho\n'
            assert res.finished
            assert res.ok
