import ams_compiler as compiler
def main():
    pass

def compile(infile, outfile):
    with open(infile, "r", encoding = "utf-8") as file:
        text = file.read()

    file = text.split("\n")

    tree_list = compiler.build_tree(file)
    out_text = compiler.compile_tree_list(tree_list)

    with open(outfile, "w", encoding = "utf-8") as file:
        file.write(out_text)


if __name__ == '__main__':
    main()
