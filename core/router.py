from tkinter.ttk import Frame
from routes.main import create_routes

import tkinter as tk


class Router:
    def __init__(self, app):
        self.app = app
        self.routes = {}
        self.current_frame = None
        self.current_route = ''

        create_routes(self)

    def add_route(self, name: str, pageClass):
        self.routes[name] = pageClass

    def rerender(self):
        self.push(self.current_route)

    def push(self, new_route: str, **kwargs):
        self.current_route = new_route

        page = self.routes[new_route](**kwargs)

        if self.current_frame is not None:
            self.current_frame.destroy()

        frame = tk.Frame(self.app.root)
        page.frame(self.app, frame)

        self.current_frame = frame
