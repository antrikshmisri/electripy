"""Module for the creation of the elements."""
from abc import ABC, abstractmethod
from hashlib import md5

import numpy as np

from electripy.utils import __all_ui__ as all_ui


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

    def __init__(self, name, position, parent=None):
        """Initialize the element.
        
        Parameters
        ----------
        name : str
            The name of the element.
        position : tuple
            The absolute position of the element.
        parent : :class: `Element`
            The parent element.
        """
        self.name = name
        self.parent = parent
        self.children = []
        self.attributes = {}

        self._position = tuple()
        self.position = position

        if self.name not in all_ui:
            raise ValueError(f'{self.name} has not been implemented.')

        if self.parent:
            self.parent.add_child(self, position)
        
        self._process_attributes()

    def _process_attributes(self):
        """Process the attributes of the element."""
        self.attributes['id'] = md5(self.name.encode()).hexdigest()
        self.attributes['class'] = self.name

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

            position = tuple(self.position[i] + position[i] for i in range(2))
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
    def _add_to_app(self, app):
        """Add the element and its children to the app."""
        _msg = '_add_to_app() must be implemented.'
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
