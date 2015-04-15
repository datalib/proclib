from pytest import fixture
from procs.pipe import Pipe


@fixture
def pipe():
    return Pipe(
            [['cat'], ['grep', 'at']],
            data='ca\nat\n',
            hooks={'success': [lambda k: 1]}
            )


def test_order(pipe):
    assert list(pipe.order()) == [['grep', 'at'], ['cat']]


def test_make_process(pipe):
    proc = pipe.make_process(['echo', 'hi'])

    assert proc.hooks == pipe.hooks
    assert proc.run().stdout == 'hi\n'


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
