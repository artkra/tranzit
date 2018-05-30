import os
import sys
import shutil
from subprocess import call


def cli_handler():
    _args = sys.argv

    _handle_dict = {
        'run': _run,
        'project': _make_starter
    }

    def _tip():
        print('''
    This is a little TRANZIT cli tool.

    Usage:
        $ tranzit project <PROJECT_NAME>  | creates a new tranzit project skeleton
        $ tranzit run                     | runs a project (must be in a project directory where main.py is)

        ''')

    if len(_args) == 1:
        _tip()

    else:
        try:
            if len(_args) > 2:
                _handler_args = _args[2:]
            else:
                _handler_args = ()
            _handle_dict[_args[1]](*_handler_args)
        except KeyError:
            _tip()
        except TypeError:
            _tip()


def _run():
    call(['python', 'main.py'])


def _make_starter(dir_name):
    src = os.path.join(os.path.dirname(__file__), 'starter')
    dst = os.path.join(os.getcwd(), dir_name)

    shutil.copytree(src, dst, symlinks=False, ignore=None)

    print('\n[INFO] Created new tranzit project: {}\n'.format(dir_name))
    print('To run a project:\n  $ cd {} && tranzit run\n'.format(dir_name))
