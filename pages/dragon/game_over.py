import tkinter as tk
from PIL import Image, ImageTk
#from pygame import mixer


class DragonGameOverPage:

    def __init__(self):
        self.left_head_path = 'assets/images/left_head_fire.png'
        self.right_head_path = 'assets/images/right_head_fire.png'
        self.middle_head_path = 'assets/images/3headDragon.png'

        # mixer.init()
        # mixer.music.load('assets/voices/fire_breath.mp3')

    def frame(self, app, frame: tk.Frame):
        frame.grid()
        frame.pack()

        riddle_num = app.get_state('riddle')
        img_path = self.left_head_path
        if riddle_num == 1:
            img_path = self.middle_head_path
        elif riddle_num == 2:
            img_path = self.right_head_path

        img = Image.open(img_path)
        img = img.resize((800, 800))
        photo = ImageTk.PhotoImage(img)
        # mixer.music.play()

        frame.photo = photo

        canvas = tk.Canvas(frame, width=800, height=800)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=photo, anchor='nw')

        canvas.create_text(400, 450, text='You\'re done Traveler!', fill='#FCFEE2',
                    font=app.theme['fonts'].dragon_default_font, anchor='center', width=400)

        frame.after(1,  app.root.destroy())
