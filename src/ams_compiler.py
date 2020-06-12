def build_tree(file, debug = False):
    """
    Takes in a list of strings and builds a command tree from it.
    Each child gets defined with one indent (Tab) more than it's parent. Example:

    execute if condition1
        if condition2
            run command 1
            run command 2
        if condition3
            run command 1
            run command 2
    """

    line = 0
    tree_list = []

    while line < len(file):
        # Get current command
        command = file[line]

        # SKip empty and comments
        if len(command.strip()) == 0 or command.strip().startswith("#") or len(file) == line:
            line += 1
            continue

        next_tree, line = __build_element__(file, line, debug = debug)

        tree_list.append(next_tree)

    return tree_list


def __build_element__(file, line, debug = False):
    """
    Look at given line of file. if it's a comment or it's empty, skip it.

    Then look at all following lines. If the indent is greater than the current on, execute __build_element__ on the next line and add the returned element as a child. The returned line is the next line to be checked.

    If the indent is equal or smaller return
    """
    # Get current command
    command = file[line]

    # If empty or end of file return
    if len(command) == 0 or command.strip().startswith("#") or len(file) == line:
        return None, line

    # Count indents and cast to node
    #indent = command.count(indent_marker)
    indent = __count_indents__(command)
    current_element = node(command.replace(indent_marker, ""))

    next_line = line+1

    #As long as you have not reached end of file
    while next_line != len(file):
        if debug:
            print("Line: ", next_line, indent_marker, file[next_line])
        # Add all children
        next_command = file[next_line]
        #Skip empty or commented lines
        if len(next_command.strip()) == 0 or next_command.strip().startswith("#"):
            next_line += 1
            continue

        #next_indent = next_command.count("\t")
        next_indent = __count_indents__(next_command)

        if next_indent > indent:
            next_child, next_line = __build_element__(file, next_line)
            current_element.add_child(next_child)
        else:
            break



    return current_element, next_line


def compile_tree_list(tree_list):
    """
    Compiles node.compile for each element in the list and
    compiles the string to be pasted into the file.
    """
    compiled_list = []
    for tree in tree_list:
        compiled_list += tree.compile()

    compiled_string = ""
    for element in compiled_list:
        compiled_string += element+"\n"

    return compiled_string


def __count_indents__(string):
    # Accept either "\t" or " " as indent.

    indent_chars = ["\t", " "]

    indents = 0
    for char in string:
        if char in indent_chars:
            indents += 1
        else:
            break

    return indents

class marker:
    def __init__(self, string):
        self.string = string

    def add_child():
        pass

    def to_str(self, n=1):
        return self.string

    def compile(self, parent = ""):
        pass

class node:
    """
    Tree Node for command tree.
    """

    def __init__(self, string):
        self.string = string
        self.children = []

    def add_child(self, child):
        """
        Accepts either Strings or cmd_node objects. Adds child to children list
        """

        if type(child) == str:
            child = node(child)

        self.children.append(child)

    def to_str(self, n=1):
        """
        Bakes String of self and all children
        """
        #print(n)
        ret_str = self.string
        for child in self.children:
            ret_str += "\n"+"\t"*n+child.to_str(n+1)

        return ret_str

    def compile(self, parent = ""):
        """
        Compiles tree into list. Example:
        execute if condition
            run command1
            run command2

        gets compiled to:
        [
            execute if condition run command1,
            execute if condition run command2
        ]
        """
        next_str = parent + self.string + " "
        next_list = []


        if len(self.children) > 0:
            for child in self.children:
                next_list += child.compile(next_str)

            return next_list
        else:
            return [next_str]
