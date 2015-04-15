from proclib.helpers import str_parse, list_parse,\
        convert_args, dispatch_hook


def test_str_parse():
    assert str_parse('cat') == [['cat']]
    assert str_parse('cat | grep') == [['cat'], ['grep']]


def test_list_parse():
    assert list_parse(['cat', 'grep']) == [['cat'], ['grep']]
    assert list_parse([['cat'], 'grep']) == [['cat'], ['grep']]
    assert list_parse(['cat', 'grep at']) == [['cat'], ['grep', 'at']]


def test_convert_args():
    assert convert_args([['cat'], ['grep']]) == [['cat'], ['grep']]
    assert convert_args(['cat', ['grep']]) == [['cat'], ['grep']]
    assert convert_args('cat | grep') == [['cat'], ['grep']]


def test_dispatch_hook_silent_error():
    assert dispatch_hook({}, 's', 1) == 1


def test_dispatch_hook_calls_hooks():
    ctx = []
    assert dispatch_hook({'s': [ctx.append]}, 's', 1) == 1
    assert ctx == [1]
