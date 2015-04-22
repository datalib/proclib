from itertools import chain
from pytest import fixture
from proclib.pipe import Pipe, make_response
from proclib.process import Process


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


@fixture(scope='module')
def res(request):
    r = Pipe([['yes'], ['head', '-n', '2']]).run()
    r.wait()
    request.addfinalizer(r.close)
    return r


def test_sigpipe_was_used(res):
    yes = res.history[0]
    yes.wait()
    assert yes.explain()['signal'] == 'SIGPIPE'
    assert not yes.ok


def test_correct_data(res):
    assert len(res.out.split()) == 2
    assert res.ok


def test_make_response_pops_proc():
    procs = chain(
        [Process(['echo', 'm']) for _ in range(2)],
        [Process(['echo', 'a'])],
        )
    r = make_response(procs)

    assert len(r.history) == 2
    assert r.out == 'a\n'
    assert r.command == ['echo', 'a']
