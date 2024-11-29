from tkinter import Tk

from core.router import Router
from core.fonts import Fonts
from core.colors import Colors


class App:
    def __init__(self, puzzle, *args, **kwargs):
        self.root = Tk()
        self.states = {}
        self.theme = {'fonts': Fonts(self.root), 'colors': Colors}

        self.init_window()

        self.router = Router(self)
        self.router.push(puzzle, **kwargs)

    def init_window(self):
        self.root.geometry("800x800")
        self.root.resizable(0, 0)

    def update_geometry(self, a):
        self.root.geometry(a)

    def update_title(self, title):
        self.root.title(title)

    def update_bg_color(self, color):
        self.root.configure(bg=color)

    def push(self, route: str, **kwargs):
        self.router.push(route)

    def get_state(self, key: str, defaultValue=None):
        if key in self.states:
            return self.states[key]
        else:
            self.states[key] = defaultValue
            return defaultValue

    def set_state_rerender(self, key: str, value):
        self.states[key] = value

        self.router.rerender()

    def set_state(self, key: str, value):
        self.states[key] = value

    def run(self):
        self.root.mainloop()
