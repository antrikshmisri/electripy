import numpy.testing as npt
from electripy.elements import Button, Element, Paragraph


def test_element():
    class BaseElement(Element):
        def __init__(self, name, position, parent=None):
            super(BaseElement, self).__init__(name, position, parent)

        def _get_element_tree(self):
            return {self.name: self.children}

        def _add_to_app(self, app):
            return

        def _setup(self):
            pass

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

        def _setup(self):
            pass

    with npt.assert_raises(ValueError):
        _ = InvalidElement('InvalidElement', (0, 0))


def test_button():
    basic_btn = Button('This is a button')

    npt.assert_equal(basic_btn.name, 'Button')
    npt.assert_equal(basic_btn.children[0].name, 'Paragraph')
    npt.assert_equal(basic_btn.children[0].text, 'This is a button')

    basic_btn_style = basic_btn._parse_style()
    btn_para_style = basic_btn.children[0]._parse_style()

    npt.assert_equal(basic_btn_style['position'], 'relative')
    npt.assert_equal(btn_para_style['position'], 'absolute')
    npt.assert_equal(btn_para_style['left'], '10%')
    npt.assert_equal(btn_para_style['bottom'], '50%')

    icon_btn = Button('This is a button', icon_name='add')
    icon_url = icon_btn.icon_url_dict['add']

    npt.assert_equal(icon_btn.icon.src, icon_url)
    npt.assert_equal(icon_btn.icon.size, (50, 50))

    icon_style = icon_btn.icon._parse_style()

    npt.assert_equal(icon_style['position'], 'absolute')
    npt.assert_equal(icon_style['left'], '90%')
    npt.assert_equal(icon_style['bottom'], '50%')


def test_paragraph():
    para = Paragraph('This is a paragraph')
    npt.assert_equal(para.text, 'This is a paragraph')

    para_style = para._parse_style()
    npt.assert_equal(para_style['position'], 'absolute')
    npt.assert_equal(para_style['font-size'], '10px')

    para.text = 'This is a new paragraph'
    npt.assert_equal(para.text, 'This is a new paragraph')
