import shlex


def str_parse(cmds):
    args = []
    buff = []
    for item in shlex.split(cmds):
        if item == '|':
            args.append(buff)
            buff = []
            continue
        buff.append(item)

    if buff:
        args.append(buff)
    return args


def list_parse(cmds):
    args = []
    for item in cmds:
        if isinstance(item, str):
            args.append(shlex.split(item))
            continue
        args.append(item)
    return args


def convert_args(cmds):
    if isinstance(cmds, str):
        return str_parse(cmds)
    return list_parse(cmds)
