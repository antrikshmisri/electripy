__all_ui__ = {
    'Button',
    'Paragraph',
    'Heading',
    'Image',
}


def log_element_recursive(element, depth=0, out=""):
    tree = element._get_element_tree()

    for item in tree.items():
        name = item[0].name
        children = item[1]

        out += f"|{'===>' * depth} <{name} class={item[0].attributes['class']} id={item[0].attributes['id']}>\n"

        if children:
            for child in children:
                out = log_element_recursive(child, depth + 1, out)
    
    return out
