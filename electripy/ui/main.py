import os
import sys

try:
    from electripy import eel
    from electripy.ui.utils import (IN_DEVELOPMENT, fetch_npm_package,
                                get_electron_bin, shutdown)

except ImportError:
    currentdir = os.path.dirname(os.path.abspath(__file__))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, os.path.dirname(parentdir))

    from electripy import eel
    from electripy.ui.utils import (IN_DEVELOPMENT, fetch_npm_package,
                                get_electron_bin, shutdown)


EEL_PORT = 8888
FRONTEND_PORT = 3000


def init_ui(eel_port, frontend_port):
    """Initialize the UI.

    Parameters
    ----------
    eel_port: int
        The port to use for the EEL server.
    frontend_port: int
        The port to use for the frontend server.
    """
    if not all([eel_port, frontend_port]):
        raise ValueError('Both ports must be specified.')

    if IN_DEVELOPMENT:
        _electron_path = os.path.join(
            os.getcwd(), 'electripy', 'ui', "node_modules/electron/dist/electron.exe")
        if not os.path.isfile(_electron_path):
            raise Exception(
                f'Electron not found in path {_electron_path}.\n')

        eel.init("./src")
        eel.browsers.set_path('electron', _electron_path)
        eel.start({
            'port': frontend_port,
        }, options={
            'port': eel_port,
            'host': 'localhost',
            'args': [_electron_path, '.'],
        }, suppress_error=True, size=(1000, 600), mode="electron")
    else:
        _electron_path = get_electron_bin()

        if not os.path.isfile(_electron_path):
            print('Warning: Electron not found in global packages\n'
                  'Trying to install through npm....')

            npm_out = fetch_npm_package('electron')
            if not len(npm_out):
                raise Exception(
                    "Something went wrong, couldn't install electron.")
            else:
                print(npm_out[:100] + '...')

        print(_electron_path)
        eel.init('build')
        eel.browsers.set_path('electron', _electron_path)
        eel.start('',
                  options={
                      'port': eel_port,
                      'host': 'localhost',
                      'close_callback': shutdown,
                      'args': [_electron_path, '.'],
                  }, suppress_error=True, size=(1000, 600), mode="electron")


if __name__ == '__main__':
    init_ui(eel_port=EEL_PORT, frontend_port=FRONTEND_PORT)
