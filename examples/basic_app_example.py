"""
=========================================
Example to how to initialize an App with
different UI elements in it.
=========================================

In this example we will create a simple App with
different UI elements in it. First, some imports:
"""
from electripy.app import App
from electripy.elements import Button
from electripy.elements.core import Body

btn = Button('Button', font_size=15,
             class_name='btn', position=(100, 100),
             icon_name='add')


app = App(root=Body(padding=(10, 10)), title="Test App")
app.add_element(btn)

app.start()
