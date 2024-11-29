import tkinter as tk
from PIL import Image, ImageTk
import time
from pygame import mixer


class DragonGameOverPage:

    def __init__(self):
        self.left_head_path = 'assets/images/left_head_fire.png'
        self.right_head_path = 'assets/images/right_head_fire.png'
        self.middle_head_path = 'assets/images/3headDragon.png'

        mixer.music.load('assets/voices/fire_breath.mp3')
        self.close_btn_img = ImageTk.PhotoImage(
            Image.open('assets/images/close.png').resize((50, 50)))


    def frame(self, app, frame: tk.Frame):
        frame.grid()
        frame.pack()
        self.dark_blue = app.theme['colors'].dark_blue
        self.btn_color = app.theme['colors'].btn_color
        self.success_color_purple = app.theme['colors'].success_color_purple
        self.error_color_pink = app.theme['colors'].error_color_pink
        self.title_font = app.theme['fonts'].hat_title_font

        riddle_num = app.get_state('riddle')
        img_path = self.left_head_path
        if riddle_num == 1:
            img_path = self.middle_head_path
        elif riddle_num == 2:
            img_path = self.right_head_path

        img = Image.open(img_path)
        img = img.resize((800, 800))
        photo = ImageTk.PhotoImage(img)
        mixer.music.play()

        frame.photo = photo

        canvas = tk.Canvas(frame, width=800, height=800)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=photo, anchor='nw')

        canvas.create_text(400, 450, text='You\'re done Traveler!', fill='#FCFEE2',
                    font=app.theme['fonts'].dragon_default_font, anchor='center', width=400)
        
        self.show_message(
                    frame, app, "Wrong!", "You missed the puzzle!", self.error_color_pink)
        #frame.after(1,  app.root.destroy())
        
    def show_message(self, frame, app, title, message, color):
        frame.grid()
        frame.pack()

        msg_box = tk.Toplevel(frame)
        msg_box.geometry("300x150")
        msg_box.config(bg=self.dark_blue)
        msg_box.title(title)

        # Label for the message content with the custom font
        label = tk.Label(msg_box, text=message,
                         font=self.title_font, fg=color, bg=self.dark_blue)
        label.pack(pady=20)

        canvas = tk.Canvas(msg_box, width=300, height=100,
                           bg=self.dark_blue, highlightthickness=0)
        canvas.pack()
        close_btn = canvas.create_image(
            150, 40, image=self.close_btn_img, anchor='center')

        canvas.tag_bind(
            close_btn, "<Button-1>", lambda event: (msg_box.destroy(), app.root.destroy()))
