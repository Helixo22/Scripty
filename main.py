from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFontDialog, QVBoxLayout, QPushButton, QLabel, QWidget, QStyleFactory
from PyQt5.QtGui import QTextCursor, QFont

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scripty")
        self.setGeometry(100, 100, 800, 600)

        self.text_widget = QTextEdit(self)
        self.setCentralWidget(self.text_widget)

        self.create_menus()

        self.theme = {
            "default": {"bg": "white", "fg": "black"},
            "forest": {"bg": "#C3E5CB", "fg": "#205F3D"},
            "dracula": {"bg": "#282a36", "fg": "#f8f8f2"},
            "dark": {"bg": "#2d2d2d", "fg": "#ffffff"}
        }

        self.current_theme = "default"
        self.apply_theme()

        self.bold_tags = {"bold": QFont()}
        self.bold_tags["bold"].setBold(True)
        self.italic_tags = {"italic": QFont()}
        self.italic_tags["italic"].setItalic(True)

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open", self.open_file)
        file_menu.addAction("Save", self.save_file)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo", self.text_widget.undo)
        edit_menu.addAction("Redo", self.text_widget.redo)
        edit_menu.addSeparator()
        edit_menu.addAction("Cut", self.text_widget.cut)
        edit_menu.addAction("Copy", self.text_widget.copy)
        edit_menu.addAction("Paste", self.text_widget.paste)
        edit_menu.addSeparator()
        edit_menu.addAction("Bold", self.toggle_bold)
        edit_menu.addAction("Italic", self.toggle_italic)

        theme_menu = menubar.addMenu("Themes")
        theme_menu.addAction("Default", lambda: self.change_theme("default"))
        theme_menu.addAction("Forest", lambda: self.change_theme("forest"))
        theme_menu.addAction("Dracula", lambda: self.change_theme("dracula"))
        theme_menu.addAction("Dark", lambda: self.change_theme("dark"))

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.text_widget.setPlainText(file_content)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.toPlainText())

    def toggle_format(self, format_type):
        cursor = self.text_widget.textCursor()
        cursor.beginEditBlock()

        char_format = cursor.charFormat()

        if format_type == "bold":
            char_format.setFontWeight(QFont.Bold if char_format.fontWeight() != QFont.Bold else QFont.Normal)
        elif format_type == "italic":
            char_format.setFontItalic(not char_format.fontItalic())

        cursor.mergeCharFormat(char_format)
        cursor.endEditBlock()

    def toggle_bold(self):
        self.toggle_format("bold")

    def toggle_italic(self):
        self.toggle_format("italic")

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme.get(self.current_theme, self.theme["default"])
        self.text_widget.setStyleSheet(f"background-color: {theme['bg']}; color: {theme['fg']};")
        self.setStyle(QStyleFactory.create("Fusion"))

if __name__ == "__main__":
    app = QApplication([])
    notepad = Notepad()
    notepad.show()
    app.exec_()
