"""Module that provides the main application and some other app related methods."""

import os
from electripy.elements.core import Body
from electripy.ui.main import EEL_PORT, FRONTEND_PORT, init_ui
from electripy.ui.utils import IN_DEVELOPMENT
from electripy.utils import execute_command


class App:
    """Class to represent the main application"""

    def __init__(self, root=None, title="Electripy Application", size=(1000, 600),
                 transparent=True, rounded_corners=True, window_shadow=True,
                 resizable=False, icon_path=None):
        """Initialize the application.
        
        Parameters
        ----------
        root: :class: `Body`, optional
            The root element of the application.
        title: str, optional
            The title of the application.
        size: tuple, optional
            The size of the application.
        transparent: bool, optional
            Whether the application is transparent or not.
        rounded_corners: bool, optional
            Whether the application has rounded corners or not.
        window_shadow: bool, optional
            Whether the application has window shadow or not.
        resizable: bool, optional
            Whether the application is resizable or not.
        icon_path: str, optional
            The path of the icon to display in the application.
        """
        self.root = root or Body(padding=(10, 10))
        self.title = title
        self.size = size
        self.transparent = transparent
        self.rounded_corners = rounded_corners
        self.window_shadow = window_shadow
        self.resizable = resizable
        self.icon_path = icon_path or './ui/public/logo.png'

        self._config = {}
        self.add_configurations(eel_port=EEL_PORT, frontend_port=FRONTEND_PORT)

    def __str__(self):
        """Return the string representation of the application."""
        return f"<App title={self.title} size={self.size}"\
                f" transparent={self.transparent} rounded_corners={self.rounded_corners}"\
                f" window_shadow={self.window_shadow} resizable={self.resizable}"\
                f" icon_path={self.icon_path}>"\
                f"\n{self.root}"


    def add_element(self, element):
        """Add an element to the root of the application.
        
        Parameters
        ----------
        element: :class: `Element`
            The element to be added
        """
        element.add_to_app(self)
    
    def add_configurations(self, eel_port, frontend_port):
        """Add configurations to the application.
        
        Parameters
        ----------
        eel_port: int
            The port to use for the EEL server.
        frontend_port: int
            The port to use for the frontend server.
        """
        EEL_PORT = eel_port
        FRONTEND_PORT = frontend_port

        self._config.update({
            'eel_port': EEL_PORT,
            'frontend_port': FRONTEND_PORT
        })
    
    def start(self, in_development=IN_DEVELOPMENT):
        """Start the application."""
        if in_development:
            print('Starting Electripy in development mode...')
            _current_dir = os.getcwd()
            os.chdir(os.path.join(os.getcwd(), 'electripy', 'ui'))
            for line in execute_command('yarn start'):
                print(line, end='')
                if 'exited' in line:
                    os.chdir(_current_dir)
                    exit(0)
            os.chdir(_current_dir)
        else:
            init_ui(**self._config)