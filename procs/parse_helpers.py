import shlex


def str_parse(cmds):
    buff = []
    for item in shlex.split(cmds):
        if item == '|':
            yield buff
            buff = []
            continue
        buff.append(item)

    if buff:
        yield buff


def list_parse(cmds):
    for item in cmds:
        if isinstance(item, str):
            yield shlex.split(item)
            continue
        yield item


def convert_args(cmds):
    if isinstance(cmds, str):
        return str_parse(cmds)
    return list_parse(cmds)
