import os
from abc import ABC, abstractmethod
from hashlib import md5
from urllib.request import urlretrieve

import numpy as np
from electripy import eel
from electripy.utils import __all_ui__ as all_ui
from electripy.utils import log_element_recursive
from PIL import Image as PILImage


class Element(ABC):
    """Base class for all UI elements.

    Attributes
    ----------
    name : str
        The name of the element.
    parent : :class: `Element`
        The parent element.
    children : list
        The children of the element.
    attributes : dict
        The attributes of the element.
    """

    def __init__(self, name, position=(0, 0), parent=None, class_name=None):
        """Initialize the element.

        Parameters
        ----------
        name : str
            The name of the element.
        position : tuple, optional
            The absolute position of the element.
        parent : :class: `Element`, optional
            The parent element.
        class_name : str, optional
            The class name of the element.
        """
        self.children = []
        self.attributes = {}

        self.name = name
        if self.name not in all_ui:
            raise ValueError(
                f'{self.name} has not been implemented, add it to __all_ui__.')

        self._class_name = str
        self.class_name = class_name or ''

        self.parent = parent
        if self.parent:
            self.parent.add_child(self, position)

        self._position = tuple()
        self.position = position

        self._callbacks = {
            'onClick': None,
            'onChange': None,
            'onFocus': None,
            'onBlur': None,
            'onKeyPress': None
        }

        self._process_attributes()
        self._setup()
        self._expose_callbacks()

    def __str__(self):
        """Return the string representation of the element."""
        return log_element_recursive(self)

    @abstractmethod
    def _setup(self):
        """Setup the element."""
        _msg = f'{self.name} has not been implemented.'
        raise NotImplementedError(_msg)

    def _process_attributes(self):
        """Process the attributes of the element."""
        self.attributes['id'] = md5(
            f"{self.name}{self.class_name}".encode()).hexdigest()[:5]
        self.attributes['class'] = self.class_name

    def _expose_callbacks(self):
        """Expose all event callbacks to the frontend"""
        for item in self._callbacks.items():
            _evt, _callback = item
            if _callback is None:
                continue

            _callback.__name__ = f"{self.attributes['id']}_{_evt}_callback"
            eel.expose(_callback)

    def add_callback(self, event_type, callback):
        """Add a callback associated to a specific event type.
        
        Parameters
        ----------
        event_type: str
            Type of event
        callback: function
            The callback to attach to the event
        """
        if event_type not in self._callbacks:
            raise ValueError(
                f'{event_type} is not a valid event type. Valid events are: {list(self._callbacks.keys())}')

        self._callbacks.update({event_type: callback})

    @property
    def position(self):
        """Get the position of the element."""
        return self.attributes['position']

    @position.setter
    def position(self, position):
        """Set the position of the element. Position is assumed from bottom left."""
        if len(position) == 3:
            position = tuple(position[:2])
            if self.parent:
                self.parent.add_style({'position': 'relative'})

            self.add_style({'position': 'absolute'})
            self.add_style({'left': f'{int(position[0]*100)}%'})
            self.add_style({'bottom': f'{int(position[1]*100)}%'})
        else:
            self.add_style({'position': 'absolute'})
            self.add_style({'left': f'{position[0]}px'})
            self.add_style({'bottom': f'{position[1]}px'})

        self.attributes['position'] = position
        self._position = position

    def add_child(self, child, position=(0, 0)):
        """Add a child to this element.

        Parameters
        ----------
        child : :class: `Element`
            The child to add.
        position : tuple
            The position of the child.
            If float, the child will be placed relative the parent,
            else position is assumed to be absolute.
        """
        if np.issubdtype(np.array(position).dtype, np.floating):
            if np.any(np.array(position) < 0) or np.any(np.array(position) > 1):
                raise ValueError("Normalized coordinates must be in [0,1].")

            position = (*position, 'relative')

        child.parent = self
        child.position = position
        self.children.append(child)

    def remove_child(self, child):
        """Remove a child from this element.

        Parameters
        ----------
        child : :class: `Element`
            The child to remove.
        """
        self.children.remove(child)
        child.parent = None

    @abstractmethod
    def _get_element_tree(self):
        """Get the element tree."""
        _msg = '_get_element_tree() must be implemented.'
        raise NotImplementedError(_msg)

    @abstractmethod
    def add_to_app(self, app):
        """Add the element and its children to the app."""
        _msg = 'add_to_app() must be implemented.'
        raise NotImplementedError(_msg)

    def add_style(self, style_dict):
        """Add style to the element.

        Parameters
        ----------
        style_dict : dict
            The key value pair to add the styling.
        """
        _element_style = self._parse_style()
        _element_style.update(style_dict)
        self.attributes['style'] = '; '.join(
            f'{key}: {value}' for key, value in _element_style.items())

    def _parse_style(self):
        """Parse the style of the element."""
        style_dict = {}

        if 'style' not in self.attributes:
            self.attributes['style'] = ''

        for style in self.attributes['style'].split(';'):
            if not style:
                continue
            style = style.split(':')
            style_dict[style[0].strip()] = style[1].strip()

        return style_dict

    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, class_name):
        self.attributes['class'] = class_name
        self._class_name = class_name


class Body(Element):
    """Class to represent the body."""

    def __init__(self, elements=None, padding=(0, 0)):
        """Initialize the body element.
        
        Parameter
        ---------
        elements: list of tuples
            List of (element, position) tuples
        padding: tuple
            The padding of the body.
        """
        self.elements = elements or []
        self.padding = padding
        super(Body, self).__init__(name='Body', class_name='body')

    def _setup(self):
        for element_tuple in self.elements:
            element, position = element_tuple
            self.add_child(element, position)

        self.add_style({'padding': f'{self.padding[0]}px {self.padding[1]}px'})

    def _get_element_tree(self):
        return {self: self.children}
    
    def add_to_app(self, app):
        """Add the body to the app.
        
        Parameters
        ----------
        app : :class: `App`
            The app to add the body to.
        """
        pass


class Paragraph(Element):
    """Class to represent a paragraph."""

    def __init__(self, text, font_size=10, keypress_callback=None,
                 position=(0, 0), parent=None, class_name=None):
        """Initialize the paragraph class.

        Parameters
        ----------
        text: str
            Text to display
        font_size: int, optional
            Size of the text in pixels
        keypress_callback: function, optional
            Callback function to execute when a key is pressed.
        position: tuple, optional
            The position of the paragraph.
        parent: :class: `Element`, optional
            The parent element.
        class_name: str, optional
            The class name of the paragraph.
        """
        self._text = str()
        self.text = text

        self.font_size = font_size
        self.keypress_callback = keypress_callback

        super(Paragraph, self).__init__(
            'Paragraph', position, parent, class_name)

    def _setup(self):
        """Setup this UI element."""
        self.add_style({'font-size': f'{self.font_size}px'})
        self.add_callback('onKeyPress', self.keypress_callback)

    def _get_element_tree(self):
        """Get the element tree."""
        return {self: self.children}

    def add_to_app(self, app):
        """Add the element and its children to the app."""
        app.root.add_child(self, self.position)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text


class Image(Element):
    """Class to represent an image."""

    def __init__(self, src, maintain_aspect=True, size=(100, 50),
                 alt_text=None, position=(0, 0), parent=None,
                 class_name=None):
        """Initialize the image class.

        Parameters
        ----------
        src: str
            The source of the image.
        maintain_aspect: bool, optional
            Whether to maintain the aspect ratio of the image.
        size: tuple, optional
            The size of the image.
        alt_text: str, optional
            The alt text of the image.
        position: tuple, optional
            The position of the image.
        parent: :class: `Element`, optional
            The parent element.
        class_name: str, optional
            The class name of the image.
        """
        self._img_data = None

        self.src = src
        self.is_url = 'http' in self.src.lower() or 'https' in self.src.lower()

        self.maintain_aspect = maintain_aspect
        self.size = size

        self.alt_text = alt_text or ''

        super(Image, self).__init__('Image', position, parent, class_name)

    def _setup(self):
        """Setup the Image UI element."""
        if self.is_url:
            img_path = os.path.join(
                os.getcwd(),
                f"{self.attributes['id']}.{os.path.basename(self.src).split('.')[-1]}")

            urlretrieve(self.src, img_path)
            self.img_data = PILImage.open(img_path)
        else:
            self.img_data = PILImage.open(self.src)

        if self.maintain_aspect:
            _width, _height = self.img_data.size
            _ratio = _width / _height

            _new_width = self.size[0]
            _new_height = self.size[1]

            if _ratio > 1:
                _new_height = int(_new_width / _ratio)
            else:
                _new_width = int(_new_height * _ratio)

            self.img_data = self.img_data.resize((_new_width, _new_height))

            self.size = (_new_width, _new_height)
            self.add_style({'width': f'{_new_width}px',
                            'height': f'{_new_height}px'})
        else:
            self.add_style({'width': f'{self.size[0]}px',
                            'height': f'{self.size[1]}px'})

            self.img_data = self.img_data.resize(self.size)

        self.attributes['alt'] = self.alt_text
        self.attributes['src'] = self.src

    def _get_element_tree(self):
        """Get the element tree."""
        return {self: self.children}

    def add_to_app(self, app):
        """Add the element and its children to the app."""
        app.root.add_child(self, self.position)

    @property
    def img_data(self):
        return self._img_data

    @img_data.setter
    def img_data(self, img_data):
        self._img_data = img_data
