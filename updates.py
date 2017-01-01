import re
import subprocess


PYTHON_REGEX = re.compile(r'^([\w\.\-]+) \(')


def call(cmd):
    subprocess.check_call(cmd.split())


def call_with_output(cmd):
    return subprocess.check_output(cmd.split())


def update_brew():
    call('brew update')
    call('brew upgrade')
    call('brew cleanup')


def update_vim():
    call('vim -i NONE -c PlugUpgrade -c PlugUpdate -c quitall')


def update_node():
    call('npm update -g')


def update_python(platform):

    def update_package(package):
        print 'Updating package: {}'.format(package)
        call_with_output('{} install -U {}'.format(platform, package))

    def parse_line(line):
        if '' == line.strip():
            return
        match = PYTHON_REGEX.match(line)
        if match is None:
            print 'Could not find package: {}'.format(line)
        else:
            name = match.group(1)
            update_package(name)

    assert platform in ['pip2', 'pip3']
    map(parse_line,
        call_with_output('{} list --outdated --format=legacy'.format(platform))
            .splitlines())


def update_ocaml():
    call('opam update')
    call('opam upgrade')


def run_all_updaters():

    def call_update(name, update):
        print '--------------------'
        print 'Updating {}'.format(name)
        update()

    def call_updater(entry):
        name, update, args = entry
        if args is None:
            call_update(name, update)
        else:
            map(lambda (arg_name, arg): call_update(arg_name, lambda: update(arg)), args)

    updaters = [
        ('brew', update_brew, None),
        ('python', update_python, [('python2', 'pip2'), ('python3', 'pip3')]),
        ('node', update_node, None),
        ('ocaml', update_ocaml, None),
        ('vim', update_vim, None),
    ]
    map(call_updater, updaters)


if '__main__' == __name__:
    run_all_updaters()
