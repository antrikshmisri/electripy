import numpy.testing as npt
from electripy.elements import Image, Paragraph
from electripy.utils import log_element_recursive


def test_log_element():
    img = Image(src="https://img.icons8.com/ios-glyphs/50/000000/python.png",
                class_name="python-icon")

    img_caption = Paragraph("This is the caption for the image", font_size=15,
                            class_name='image-caption')

    img.add_child(img_caption, (0.5, 1.0))

    out = log_element_recursive(img)
    npt.assert_equal(
        f"<Image class={img.class_name} id={img.attributes['id']}>\n" in out,
        True)
    
    npt.assert_equal(
        f"<Paragraph class={img_caption.class_name} id={img_caption.attributes['id']}>\n" in out,
        True)

