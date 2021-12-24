import numpy.testing as npt
from electripy.elements import Element


def test_element():
    class BaseElement(Element):
        def __init__(self, name, position, parent=None):
            super(BaseElement, self).__init__(name, position, parent)

        def _get_element_tree(self):
            return {self.name: self.children}

        def _add_to_app(self, app):
            return

    base_element = BaseElement('Button', (0, 0))
    child_element = BaseElement('Paragraph', (0, 0))

    base_element.add_child(child_element, (100, 100))

    npt.assert_equal(base_element.children[0].name, 'Paragraph')

    style_dict = base_element._parse_style()

    npt.assert_equal(style_dict['position'], 'absolute')
    npt.assert_equal(style_dict['left'], '0px')
    npt.assert_equal(style_dict['bottom'], '0px')

    child_style_dict = child_element._parse_style()

    npt.assert_equal(child_style_dict['position'], 'absolute')
    npt.assert_equal(child_style_dict['left'], '100px')
    npt.assert_equal(child_style_dict['bottom'], '100px')

    base_element.remove_child(child_element)

    npt.assert_equal(base_element.children, [])
    base_element.add_child(child_element, (0.5, 0.5))

    style_dict = base_element._parse_style()

    npt.assert_equal(style_dict['position'], 'relative')
    npt.assert_equal(style_dict['left'], '0px')
    npt.assert_equal(style_dict['bottom'], '0px')

    child_style_dict = child_element._parse_style()

    npt.assert_equal(child_style_dict['position'], 'absolute')
    npt.assert_equal(child_style_dict['left'], '50%')
    npt.assert_equal(child_style_dict['bottom'], '50%')

    base_element.add_style({'position': 'absolute'})
    npt.assert_equal(base_element._parse_style()['position'], 'absolute')

    class InvalidElement(Element):
        def __init__(self, name, position, parent=None):
            super(InvalidElement, self).__init__(name, position, parent)

        def _get_element_tree(self):
            return {self.name: self.children}

        def _add_to_app(self, app):
            return

    with npt.assert_raises(ValueError):
        _ = InvalidElement('InvalidElement', (0, 0))
