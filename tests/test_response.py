from procs.response import Response


def test_response():
    r = Response(
        command=['command'],
        process=None,
        stdout='a',
        stderr='b',
        returncode=1,
        pid=100)

    assert r.pid == 100
    assert r.returncode == 1
    assert r.stdout == 'a'
    assert r.stderr == 'b'
    assert not r.ok

    r.returncode = 0
    assert r.ok
