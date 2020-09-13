import warnings

help_str = """
ams transpiler is designed for mincraft mcfunctions to be transformed from a more human readable version into a minecraft runnable version.

-h
--h
--help  Show this message

===========================

-c  Provide a config file.
    ams -c [filename]

-i  Provide input file.
    Not compatible with -c
    ams -i [filename]

 -o Provide an output file
    Not Compatible with -c.
    Must first provide input file with -i [filename]
    ams -i [filename] -o [filename]
"""

def main():
    import json
    from sys import argv as args

    # Initialiizing to read args from command line
    arg_pointer = 1

    cdict = {}
    config = False
    input = False
    output = False

    # import args from command line

    if len(args) == 1:
        raise ValueError("Must provide args. Type 'ams -h' for help.")

    if args[arg_pointer] == "-h" or args[arg_pointer] == "--h" or args[arg_pointer] == "--help":
        print(help_str)
        exit()

    while arg_pointer < len(args):

        if args[arg_pointer] == "-c":
            config = True
            try:
                cfile = args[arg_pointer+1]
                print(cfile)
            except:
                raise ValueError("Please supply a config file")

            arg_pointer += 2
            continue

        if args[arg_pointer] == "-i" and config == False:

            input = True
            try:
                cdict["ifiles"] = [args[arg_pointer+1]]
                if not output:
                    cdict["ofiles"] = ["out_"+args[arg_pointer+1]]
            except:
                raise ValueError("-i requires an input file.\nUsage: -i [filename]")


            arg_pointer += 2
            continue

        if args[arg_pointer] == "-o" and config == False:
            output = True

            try:
                cdict["ofiles"] = [args[arg_pointer+1]]
            except:
                raise ValueError("-o requires an input file.\nUsage: -o [filename]")

            arg_pointer += 2
            continue

        print(f"Did not recognize this argument: {args[arg_pointer]}. Ignoring...")
        arg_pointer += 1


    # Read Config file

    if config:
        try:
            with open(cfile) as file:
                loaded_config_dict = json.load(file)
        except:
            raise ValueError(f"Failed to read config file {cfile}")

        # Check Values

        if not ("ifiles" in loaded_config_dict and "ofiles" in loaded_config_dict):
            raise ValueError("Config file must provide ifiles and ofiles.")
        elif len(loaded_config_dict["ifiles"]) == len(loaded_config_dict["ofiles"]):
            raise ValueError("Number of input files must match output files")

        cdict = {**loaded_config_dict, **cdict}

    # Read and compile each file in config.
    print("Config:\n")
    print(json.dumps(cdict, indent = 2))

    for i in range(len(cdict["ifiles"])):
        in_file = cdict["ifiles"][i]
        out_file = cdict["ofiles"][i]

        print(f"Compiling {in_file}...")

        with open(in_file, "r") as inf:
            in_text = inf.read().split("\n")

        tree_list = build_tree(in_text)

        out_text = compile_tree_list(tree_list)

        with open(out_file, "w") as out:
            out.write(out_text)

        print("DONE!\n")


def build_tree(file, debug = True):
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
        if len(command.strip()) == 0:
            line += 1
            continue

        next_tree, line = __build_element__(file, line, debug = debug)

        tree_list.append(next_tree)

    return tree_list


def __build_element__(file, line, debug = False):
    """
    Look at given line of file. If it's a comment create marker, if empty skip it and if neither create node.

    Then look at all following lines. If the indent is greater than the current on, execute __build_element__ on the next line and add the returned element as a child. The returned line is the next line to be checked.

    If the indent is equal or smaller return
    """
    # Get current command
    command = file[line]

    #If empty return
    if len(command.strip()) == 0:
        return None, line

    # Count indents and cast to node
    #indent = command.count(indent_marker)
    indent = __count_indents__(command)

    if command.strip().startswith("#"):
        current_element = marker(command.strip())
    else:
        current_element = node(command.strip())

    next_line = line+1

    #As long as you have not reached end of file
    while next_line != len(file):
        if debug:
            print("Line: ", next_line, "\t", file[next_line])

        # Add all children
        next_command = file[next_line]

        if len(next_command.strip()) == 0:
            next_line += 1
            continue

        next_indent = __count_indents__(next_command)

        if next_indent > indent:
            next_child, next_line = __build_element__(file, next_line, debug)
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

    def add_child(self, child):
        warnings.warn(f"Cannot add child to comment.")

    def to_str(self, n=1):
        return self.string

    def compile(self, parent = ""):
        """
        Returns marker as while stacktrace.
        parent
            marker

        compiles to:
        [
            \"marker\"
        ]
        """
        return [self.string]

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


if __name__ == '__main__':
    main()
