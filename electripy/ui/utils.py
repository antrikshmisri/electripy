import os
from subprocess import PIPE, Popen

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
