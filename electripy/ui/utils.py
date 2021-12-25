import os
from subprocess import PIPE, Popen

import eel
import eel.browsers

IN_DEVELOPMENT = True


def fetch_npm_package(package_name):
    """Fetch a package using node package manager.
    Parameters
    ----------
    package_name: str
        Name of the package.
    """
    npm_out = Popen(f'npm install --global {package_name}',
                    stdout=PIPE, shell=True).stdout.read().decode('utf-8')

    if 'npm ERR!' in npm_out:
        print(f'Error installing {package_name}')
        return ""

    return npm_out


def get_electron_bin():
    """Get the binaries for electron using npm.
    Returns
    -------
    path
        The path to the electron binaries.
    """
    os_name = os.name
    if os_name == 'nt':
        user_path = os.path.expanduser('~')
        node_modules_path = os.path.join(
            user_path, 'AppData', 'Roaming', 'npm', 'node_modules')
        electron_path = os.path.join(
            node_modules_path, 'electron', 'dist', 'electron.exe')
        return electron_path
    elif os_name == 'posix':
        user_path = 'root'
        node_modules_path = os.path.join(
            user_path, 'local', 'lib', 'node_modules')
        electron_path = os.path.join(
            node_modules_path, 'electron', 'dist', 'electron')
        return electron_path
    else:
        raise ValueError(f'{os_name} currently not supported.')


def shutdown(path, socketlist):
    """Shutdown the UI.
    Parameters
    path: str
        The path to the UI.
    socketlist: list
        The list of sockets to close.
    """
    print(
        f"Shutting down UI with status code path: {path}, sockets: {socketlist}")
    os._exit(1)


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
            os.getcwd(), "node_modules/electron/dist/electron.exe")
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
            'close_callback': shutdown,
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
