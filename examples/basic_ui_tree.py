"""
=========================================
Example to demonstrate basic UI heirarchy
=========================================

In this example we will create a simple UI heirarchy.
First, some imports:
"""
from electripy.elements import Button, Image, Paragraph

btn = Button('This is a button', font_size=15,
             class_name='btn', position=(100, 100),
             icon_name='add')

preceeding_icon = Image(
    src=btn.icon_url_dict['add'], alt_text='add', class_name='preceedint-icon')
para = Paragraph('This is a paragraph', font_size=15, class_name='para')

btn.add_child(preceeding_icon, (0., 0.))
btn.icon.add_child(para, (0.5, 0.5))


def log_element(element):
    print("="*len(element.name))
    print(element.name)
    print("="*len(element.name))

    print(f"{element.name} Tree:- \n{repr(element)}")
    print(f"{element.name} Attributes:- \n{element}")


log_element(btn)
for child in btn.children:
    log_element(child)
