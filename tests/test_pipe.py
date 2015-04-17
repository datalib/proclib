from pytest import fixture
from proclib.pipe import Pipe
from proclib.response import Response


@fixture
def pipe():
    return Pipe(
            [['cat'], ['grep', 'at']],
            data=['c\nat\n'],
            )


def test_spawn_procs(pipe):
    procs = pipe.spawn_procs()
    assert [p.command for p in procs] == pipe.commands
    for p in procs:
        p.popen.kill()


def test_run_pipes_data(pipe):
    r = pipe.run()
    r.wait()
    assert r.ok
    assert r.finished
    assert r.out == 'at\n'
