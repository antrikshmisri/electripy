from subprocess import Popen, PIPE, CalledProcessError

__all_ui__ = {
    'Body',
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

        out += f"|{'===>' * depth} <{name} "
        out += f"class={item[0].attributes['class']} "
        out += f"id={item[0].attributes['id']}>\n"

        if children:
            for child in children:
                out = log_element_recursive(child, depth + 1, out)

    return out


def execute_command(command):
    """Execute a command and get continuous output.
    Parameters
    ----------
    command : str
        Command to execute.
    Yields
    ------
    line: str
        Output line.
    """
    popen = Popen(command, stdout=PIPE, stderr=PIPE,
                  shell=True, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise CalledProcessError(return_code, command)