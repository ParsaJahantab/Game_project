import tkinter as tk
from PIL import Image, ImageTk
from pygame import mixer
# from .dragons_logic import DragonsLogic


class DragonHomePage:

    def __init__(self):
        self.voice_path = 'assets/voices/dragon voice.mp3'
        self.main_img_path = 'assets/images/3headDragon.png'

        mixer.music.load('assets/voices/dragon voice.mp3')

        self.riddles = {}
        self.is_pressed = True
        self.riddles_status = {}

        self.mute_image = ImageTk.PhotoImage(
            Image.open('assets/images/mute.png'))
        self.vol_image = ImageTk.PhotoImage(
            Image.open('assets/images/volume.png'))
        self.voice_btn_color = '#081c1e'

        self.challenge_img = ImageTk.PhotoImage(
            Image.open('assets/images/challenge_not_solved.png')
        )

        self.challenge_solved_img = ImageTk.PhotoImage(
            Image.open('assets/images/challenge_solved.png')
        )
        self.challenge_btn_color = '#fefd89'

    def frame(self, app, frame: tk.Frame):        
        frame.grid()
        frame.pack()
        app.update_title('King Ghidorah\'s Riddle')

        self.set_riddles_status(app)

        if not self.riddles_status[0]:
            self.play_voice()

        # Load and display the image
        img = Image.open(self.main_img_path)
        img = img.resize((800, 800))
        photo = ImageTk.PhotoImage(img)
        frame.photo = photo

        self.canvas = tk.Canvas(frame, width=800, height=800)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, image=photo, anchor='nw')

        self.challenge_btn1 = self.create_btn(
            235, 150, self.choose_challenge_color(0), lambda event: self.go_to_riddle(app, 0))

        self.challenge_btn2 = self.create_btn(
            380, 60, self.choose_challenge_color(1), lambda event: self.go_to_riddle(app, 1))

        self.challenge_btn2 = self.create_btn(
            530, 150, self.choose_challenge_color(2), lambda event: self.go_to_riddle(app, 2))

        self.voice_btn = self.create_btn(
            20, 20, self.vol_image, self.on_voice_button_press)

    def go_to_riddle(self, app, riddle):
        if not self.check_if_possible(riddle):
            return
        app.set_state('riddle', riddle)
        self.pause_voice()
        app.push('dragon.riddle')

    def choose_challenge_color(self, riddle_num):
        if self.riddles_status[riddle_num]:
            return self.challenge_solved_img
        return self.challenge_img

    def set_riddles_status(self, app):
        for i in range(3):
            riddle_status = app.get_state(f'riddle{i}')
            self.riddles_status[i] = riddle_status if riddle_status is not None else False

    def check_if_possible(self, riddle_num):
        for i in range(0, 3):
            if riddle_num == i + 1 and not self.riddles_status[i]:
                return False
            if riddle_num == i and self.riddles_status[i]:
                return False
        return True

    def create_btn(self, width, height, icon, func):
        btn = self.canvas.create_image(width, height, image=icon)
        self.canvas.tag_bind(btn, "<Button-1>", func=func)
        return btn

    def play_voice(self):
        try:
            mixer.music.play()
            self.is_playing = True
        except Exception as e:
            print(f'Error playing music: {e}')

    def pause_voice(self):
        try:
            mixer.music.pause()
            self.is_playing = False
        except Exception as e:
            print(f'Error pausing music: {e}')

    def on_voice_button_press(self, event):
        if self.is_pressed:
            self.pause_voice()
            self.canvas.itemconfig(self.voice_btn, image=self.mute_image)
        else:
            self.play_voice()
            self.canvas.itemconfig(self.voice_btn, image=self.vol_image)
        self.is_pressed = not self.is_pressed
