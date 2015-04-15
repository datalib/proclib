from pytest import fixture
from procs.process import Process


@fixture
def proc():
    return Process('cat', data='at\n')


def test_dispatch_runs_hook(proc):
    ctx = []
    hook = ctx.append

    proc.hooks['ev'] = [hook]
    proc.dispatch('ev')

    assert ctx == [proc]


def test_popen_context_runs_error_hook(proc):
    ctx = []
    proc.hooks['error'] = [ctx.append]
    with proc.popen_context():
        proc.popen.returncode = 1

    assert ctx == [proc]


def test_popen_context_runs_success_hook(proc):
    ctx = []
    proc.hooks['success'] = [ctx.append]

    with proc.popen_context():
        proc.popen.returncode = 0

    assert ctx == [proc]


def test_run_calls_command(proc):
    r = proc.run()
    assert r.ok
    assert r.stdout == 'at\n'
    assert not r.stderr
    assert not r.history
