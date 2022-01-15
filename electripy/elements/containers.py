from electripy.elements import Element, Image, Paragraph


class Button(Element):
    """Class to represent a Button."""

    def __init__(self, button_text, press_callback=None,
                 position=(0, 0), parent=None, font_size=10,
                 size=(100, 50), class_name=None, icon_name=None):
        """Initialize the button class.

        Parameters
        ----------
        button_text: str
            Text to display inside the button
        press_callback: function, optional
            Callback function to execute when the button is pressed.
        position: tuple, optional
            The position of the button.
        parent: :class: `Element`, optional
            The parent element.
        font_size: int, optional
            The font size of the button text.
        size: tuple, optional
            The size of the button.
        class_name: str, optional
            The class name of the button.
        icon_name: str, optional
            The name of the icon to display inside the button.
            Valid names are -
            * `add`
            * `delete`
            * `edit`
            * `save`
            * `cancel`
            * `play`
            * `pause`
            * `stop`
            * `next`
            * `previous`
            * `up`
            * `down`
            * `left`
            * `right`
            * `check`
            * `uncheck`

        Note
        ----
        You can add custom icon by using the `add_icon` method.
        """
        self.name = 'Button'
        self.button_text = button_text
        self.press_callback = press_callback

        self.font_size = font_size
        self.size = size
        self.icon_name = icon_name or ''

        self.icon_url_dict = {
            'add': 'https://img.icons8.com/material-outlined/24/000000/add.png',
            'delete': 'https://img.icons8.com/material-outlined/24/000000/delete-forever.png',
            'edit': 'https://img.icons8.com/material-outlined/24/000000/edit.png',
            'save': 'https://img.icons8.com/material-outlined/24/000000/save.png',
            'cancel': 'https://img.icons8.com/material-outlined/24/000000/cancel.png',
            'play': 'https://img.icons8.com/material-outlined/24/000000/play.png',
            'pause': 'https://img.icons8.com/material-outlined/24/000000/pause.png',
            'stop': 'https://img.icons8.com/material-outlined/24/000000/stop.png',
            'next': 'https://img.icons8.com/material-outlined/24/000000/next.png',
            'previous': 'https://img.icons8.com/material-outlined/24/000000/previous.png',
            'up': 'https://img.icons8.com/material-outlined/24/000000/up-arrow.png',
            'down': 'https://img.icons8.com/material-outlined/24/000000/down-arrow.png',
            'left': 'https://img.icons8.com/material-outlined/24/000000/left-arrow.png',
            'right': 'https://img.icons8.com/material-outlined/24/000000/right-arrow.png',
            'check': 'https://img.icons8.com/material-outlined/24/000000/checkmark.png',
            'uncheck': 'https://img.icons8.com/material-outlined/24/000000/cancel.png',
        }
        super(Button, self).__init__('Button', position, parent, class_name)

    def _setup(self):
        """Setup this UI element
        
        Create the paragraph element.
        Create the icon element.
        Add icon, paragraph to the element tree.
        Add style to the element.
        Add relevant event callbacks.
        """
        self.paragraph = Paragraph(text=self.button_text,
                                   font_size=self.font_size,
                                   class_name='btn-text')

        if self.icon_name:
            self.icon = Image(src=self.icon_url_dict[self.icon_name],
                              class_name='btn-logo', maintain_aspect=True,
                              alt_text=self.icon_name)

            self.add_child(self.icon, position=(0.9, 0.5))

        self.add_child(self.paragraph, (0.1, 0.5))

        self.add_style({'width': f'{self.size[0]}px',
                        'height': f'{self.size[1]}px'})

        self.add_callback('onClick', self.press_callback)

    def _get_element_tree(self):
        """Get the element tree."""
        return {self: self.children}

    def add_to_app(self, app):
        """Add the element and its children to the app."""
        app.root.add_child(self, self.position)
