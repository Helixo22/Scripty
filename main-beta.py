import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Scripty")
        self.root.geometry("800x600")

        self.text_widget = scrolledtext.ScrolledText(self.root, wrap="word", undo=True)
        self.text_widget.pack(expand=True, fill="both")

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_widget.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_widget.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_checkbutton(label="Bold", command=self.toggle_bold)
        self.edit_menu.add_checkbutton(label="Italic", command=self.toggle_italic)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Heading 1", command=lambda: self.apply_heading(1))
        self.edit_menu.add_command(label="Heading 2", command=lambda: self.apply_heading(2))
        self.edit_menu.add_command(label="Heading 3", command=lambda: self.apply_heading(3))

        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Themes", menu=self.theme_menu)
        self.theme_menu.add_command(label="Default", command=lambda: self.change_theme("default"))
        self.theme_menu.add_command(label="Forest", command=lambda: self.change_theme("forest"))
        self.theme_menu.add_command(label="Dracula", command=lambda: self.change_theme("dracula"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))

        self.editor_mode = tk.BooleanVar()
        self.editor_mode.set(False)
        self.menu_bar.add_checkbutton(label="Editor Mode", variable=self.editor_mode, command=self.toggle_editor_mode)

        # Default theme
        self.theme = {
            "default": {"bg": "white", "fg": "black"},
            "forest": {"bg": "#C3E5CB", "fg": "#205F3D"},
            "dracula": {"bg": "#282a36", "fg": "#f8f8f2"},
            "dark": {"bg": "#2d2d2d", "fg": "#ffffff"}
        }

        self.current_theme = "default"
        self.apply_theme()

        self.line_count_label = tk.Label(self.root, text="Lines: 0")
        self.line_count_label.pack(side="bottom", anchor="e")

        
        self.text_widget.bind("<Motion>", self.update_line_count)

    def new_file(self):
        self.text_widget.delete("1.0", tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, file_content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.get("1.0", tk.END))

    def cut_text(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_widget.event_generate("<<Paste>>")

    def toggle_format(self, format_type):
        current_tags = self.text_widget.tag_names(tk.SEL_FIRST)
        if format_type in current_tags:
            self.text_widget.tag_remove(format_type, tk.SEL_FIRST, tk.SEL_LAST)
        else:
            self.text_widget.tag_add(format_type, tk.SEL_FIRST, tk.SEL_LAST)

    def toggle_bold(self):
        self.toggle_format("bold")

    def toggle_italic(self):
        self.toggle_format("italic")

    def apply_heading(self, heading_level):
        if self.text_widget.tag_ranges(tk.SEL):
            self.text_widget.tag_add(f"heading{heading_level}", tk.SEL_FIRST, tk.SEL_LAST)
        else:
            self.text_widget.tag_add(f"heading{heading_level}", "1.0", tk.END)

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme.get(self.current_theme, self.theme["default"])
        self.text_widget.config(bg=theme["bg"], fg=theme["fg"])

    def toggle_editor_mode(self):
        if self.editor_mode.get():
          
            self.text_widget.bind("<Key>", self.update_line_count_on_keypress)
        else:
            
            self.text_widget.unbind("<Key>")
            self.update_line_count()

    def update_line_count(self, event=None):
        
        line_count = self.text_widget.get("1.0", tk.END).count('\n')
        self.line_count_label.config(text=f"Lines: {line_count}")

    def update_line_count_on_keypress(self, event):
       
        self.update_line_count()

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
