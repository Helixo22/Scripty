import tkinter as tk
from tkinter import *
from tkinter import scrolledtext, font, filedialog
import tkinter as tk
from tkinter import ttk

class LandingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Scripty-home")
        self.root.geometry("400x300")

        self.label = ttk.Label(self.root, text="Welcome to Scripty", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.button = ttk.Button(self.root, text="Open Notepad", command=self.open_notepad)
        self.button.pack(pady=10)
    def open_notepad(self):
        self.root.destroy()  # Close the landing page
        notepad_root = tk.Tk()
        notepad = Notepad(notepad_root)
        notepad_root.mainloop()

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
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

        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Themes", menu=self.theme_menu)
        self.theme_menu.add_command(label="Default", command=lambda: self.change_theme("default"))
        self.theme_menu.add_command(label="Forest", command=lambda: self.change_theme("forest"))
        self.theme_menu.add_command(label="Dracula", command=lambda: self.change_theme("dracula"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))

        # Default theme
        self.theme = {
            "default": {"bg": "white", "fg": "black"},
            "forest": {"bg": "#C3E5CB", "fg": "#205F3D"},
            "dracula": {"bg": "#282a36", "fg": "#f8f8f2"},
            "dark": {"bg": "#2d2d2d", "fg": "#ffffff"}
        }

        self.current_theme = "default"
        self.apply_theme()

        self.bold_tags = {"bold": font.Font(weight=font.BOLD)}
        self.italic_tags = {"italic": font.Font(slant=font.ITALIC)}

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
        self.apply_tags()

    def toggle_italic(self):
        self.toggle_format("italic")
        self.apply_tags()

    def apply_tags(self):
        for tag, font_style in self.bold_tags.items():
            self.text_widget.tag_configure(tag, font=font_style)

        for tag, font_style in self.italic_tags.items():
            self.text_widget.tag_configure(tag, font=font_style)

        # Applica i tag al testo selezionato
        selected_text = self.text_widget.tag_names(tk.SEL_FIRST)
        if "bold" in selected_text:
            self.text_widget.tag_add("bold", tk.SEL_FIRST, tk.SEL_LAST)
        else:
            self.text_widget.tag_remove("bold", tk.SEL_FIRST, tk.SEL_LAST)

        if "italic" in selected_text:
            self.text_widget.tag_add("italic", tk.SEL_FIRST, tk.SEL_LAST)
        else:
            self.text_widget.tag_remove("italic", tk.SEL_FIRST, tk.SEL_LAST)

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme.get(self.current_theme, self.theme["default"])
        self.text_widget.config(bg=theme["bg"], fg=theme["fg"])

if __name__ == "__main__":
    root = tk.Tk()
    landing_page = LandingPage(root)
    root.mainloop()
