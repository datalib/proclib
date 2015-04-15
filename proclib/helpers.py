import shlex


def dispatch_hook(hooks, hook, data):
    if hook in hooks:
        for item in hooks[hook]:
            item(data)
    return data


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
    rv = []
    for item in cmds:
        if isinstance(item, str):
            rv.extend(str_parse(item))
            continue
        rv.append(list(item))
    return rv
