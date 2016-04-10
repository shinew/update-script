import re
import subprocess


config = {
    'brew': [],
    'vim': [],
    'python': ['pip2', 'pip3'],
}


_name_to_fn = {}


def register_updater(name):
    '''Registers an update function.

    Pass in the config key as `name`. If there are any config arguments, the
    registered function will be called once for each argument. Else, it will be
    called once without any arguments.

    '''
    assert name not in _name_to_fn, 'already added %s' % (name,)
    assert name in config, '%s not in config' % (name,)

    breaks = '--------------------'

    def g(f):
        def h(*args):
            if args:
                print '%s updating %s:%s %s' % (breaks, name, args[0], breaks)
            else:
                print '%s updating %s %s' % (breaks, name, breaks)
            f(*args)
        _name_to_fn[name] = h
        return h
    return g


@register_updater('brew')
def brew_update():
    subprocess.check_call(['brew', 'update'])
    subprocess.check_call(['brew', 'upgrade'])


@register_updater('vim')
def vim_update():
    subprocess.check_call(
        ['vim', '-i', 'NONE', '-c', 'PluginUpdate', '-c', 'quitall'])


@register_updater('python')
def python_update(platform):
    lines = subprocess.check_output(
        [platform, 'list', '--outdated']).split('\n')
    for line in lines:
        if line.strip() == '':
            continue
        match = re.match(r'^([\w\.\-]+) \(', line)
        if match is None:
            print 'Could not find package: %s' % (line,)
        else:
            name = match.group(1)
            print 'Updating package: %s' % (name,)
            output = subprocess.check_call(
                ['sudo', platform, 'install', '-U', name])


def run_all_updaters():
    for name in config:
        assert name in _name_to_fn, '%s is not registered' % (name,)
        if len(config[name]) == 0:
            _name_to_fn[name]()
        else:
            for args in config[name]:
                if type(args) is str:  # because strings are iterable
                    _name_to_fn[name](args)
                else:
                    _name_to_fn[name](*args)


if __name__ == '__main__':
    run_all_updaters()
