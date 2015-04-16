from pytest import fixture
from proclib.pipe import Pipe


@fixture
def pipe():
    return Pipe(
            [['cat'], ['grep', 'at']],
            data='ca\nat\n',
            hooks={'success': [lambda k: 1]}
            )


def test_order(pipe):
    assert list(pipe.order()) == [['grep', 'at'], ['cat']]


def test_spawn_procs(pipe):
    procs = pipe.spawn_procs()
    assert [p.command for p in procs] == pipe.commands
    assert [p.hooks for p in procs] == [pipe.hooks, pipe.hooks]
    for p in procs:
        p.popen.terminate()


def test_run_pipes_data(pipe):
    r = pipe.run()
    assert r.ok
    assert r.stdout == 'at\n'
