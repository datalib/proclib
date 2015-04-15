from procs.helpers import str_parse, list_parse, convert_args


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
