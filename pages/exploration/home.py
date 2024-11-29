from PIL import Image, ImageTk
import tkinter as tk
from pygame import mixer

from logics.exploration import ExplorationLogic


class ExplorationHomePage:

    def __init__(self, key):
        self.base_img_path = 'assets/images/locked_door5.jpg'
        self.overlay_img_path = 'assets/images/electronic_lock.png'
        self.key_img_path = 'assets/images/key.png'
        self.no_key_img_path = 'assets/images/no_key.png'
        self.combinations_path = 'assets/safe_box/combination.json'
        self.comb_bg = 'assets/images/old_img.png'

        self.close_btn_img = ImageTk.PhotoImage(
            Image.open('assets/images/close2.png').resize((50, 50))
        )
        self.has_key = key
        self.logic = ExplorationLogic(self.combinations_path)

    def frame(self, app, frame: tk.Frame):
        frame.grid()
        frame.pack()

        self.title_font = app.theme['fonts'].hat_title_font
        self.btn_font = app.theme['fonts'].hat_btn_font
        self.input_font = app.theme['fonts'].hat_input_font
        self.default_font = app.theme['fonts'].hat_default_font

        base_img = Image.open(self.base_img_path).resize((800, 800))
        overlay_image = Image.open(self.overlay_img_path).resize((100, 100))
        base_img.paste(overlay_image, (150, 300), overlay_image)
        combined_photo = ImageTk.PhotoImage(base_img)
        frame.photo = combined_photo

        self.canvas = tk.Canvas(frame, width=800, height=800)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, image=combined_photo, anchor='nw')

        key_icon = ImageTk.PhotoImage(
            Image.open(self.key_img_path).resize((100, 100)))
        if not self.has_key:
            key_icon = ImageTk.PhotoImage(
                Image.open(self.no_key_img_path).resize((100, 100)))

        frame.key_icon = key_icon

        self.canvas.create_image(20, 20, image=key_icon, anchor='nw')

        self.add_clickable_area(
            180, 310, 220, 390, lambda event: self.on_lock_click(app))
        self.add_clickable_area(
            620, 420, 700, 500, lambda event: self.on_box_click(frame, app=app))

    def add_clickable_area(self, x1, y1, x2, y2, func):
        area = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="", fill="", width=2)
        print(area)
        self.canvas.tag_bind(area, "<Button-1>", func)

    def on_lock_click(self, app):
        app.set_state('key', self.has_key)
        app.push('exploration.digital_lock')

    def on_box_click(self, frame, app):
        frame.grid()
        frame.pack()

        msg_box = tk.Toplevel(frame)
        msg_box.geometry("400x400")
        msg_box.title("Door's Combination")
        canvas = tk.Canvas(msg_box, width=400, height=400)

        if self.has_key:
            self.valid_key(msg_box=msg_box)
        else:
            self.invalid_key(msg_box=msg_box)

        canvas.pack()
        close_btn = canvas.create_image(
            200, 200, image=self.close_btn_img, anchor='center')

        canvas.tag_bind(
            close_btn, "<Button-1>", msg_box.destroy)

    def valid_key(self, msg_box):
        img = ImageTk.PhotoImage(Image.open(self.comb_bg).resize((400, 400)))
        canvas = tk.Canvas(msg_box, width=400, height=400)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=img, anchor='nw')
        msg_box.img = img

        # Label for the message content with the custom font
        canvas.create_text(
            200, 150, text=self.logic.combination['combination'], font=self.default_font, anchor='center', width=200, justify='center')
        canvas.create_text(
            200, 200, text=self.logic.combination['hint'], font=self.default_font, anchor='center', width=200, justify='center')

    def invalid_key(self, msg_box):
        msg_box.configure(bg='#fff')
        canvas = tk.Canvas(msg_box, width=400, height=400)
        canvas.pack(fill='both', expand=True)
        # canvas.create_image(0, 0, image=img, anchor='nw')
        # msg_box.img = img
        canvas.create_text(
            200, 150, text="Sorry! You don't have the key to open the safe!", font=self.default_font, anchor='center', width=200, justify='center')
