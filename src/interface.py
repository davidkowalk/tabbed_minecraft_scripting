import ams_compiler as compiler
def main():
    global tk, filedialog
    import tkinter as tk
    from tkinter import filedialog

    interface = Interface()
    interface.root.mainloop()

def compile(infile, outfile = None, debug = False):
    with open(infile, "r", encoding = "utf-8") as file:
        text = file.read()

    file = text.split("\n")


    tree_list = compiler.build_tree(file)
    if debug == True:
        for tree in tree_list:
            print(tree.to_str()+"\n\n")
    out_text = compiler.compile_tree_list(tree_list)

    if outfile is None:
        return out_text
    else:
        with open(outfile, "w", encoding = "utf-8") as file:
            file.write(out_text)

class Interface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AMS Interface")
        self.root.resizable(False, False)

        canvas = tk.Canvas(self.root, height = 500, width = 500, bg = "#282C34")
        canvas.pack(expand=True)

        self.center_frame = tk.Frame(self.root, bg = "#282C34")
        self.center_frame.place(relwidth = 0.5, relheight = 0.2, relx = 0.3, rely = 0.1)

        self.load_label = tk.Label(self.center_frame, text = "Select a File:  ", bg = "#282C34", foreground = "#DDDDDD")
        self.load_label.grid(row = 0, column = 0)
        self.load_button = tk.Button(self.center_frame, text = "Load and Compile File", command = self.compile_button, bg = "#424956", fg = "white")
        self.load_button.grid(row = 0, column = 1)

        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(2, weight=1)



    def compile_button(self):
        path = self.get_load_path()
        if path == "":
            return
        text = compile(path, debug = True)

        self.save_file(text)

    def get_load_path(self):
        return filedialog.askopenfilename(title = "Select a File", filetypes = (("MCFunction files", "*.mcfunction"), ("Text files", "*.txt*"), ("all files", "*.*")))

    def save_file(self, text):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".mcfunction")
        if f is None:
            return

        f.write(text)
        f.close()

if __name__ == '__main__':
    main()
