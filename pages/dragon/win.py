from PIL import Image, ImageTk
import tkinter as tk
from pygame import mixer


class DragonWinPage:

    def __init__(self):
        self.base_img_path = 'assets/images/win_bg.jpg'
        self.overlay_img_path = 'assets/images/win_image.png'
        self.back_icon_path = 'assets/images/arrow-left.png'
        self.final_win_path = 'assets/images/burning_wall.png'

        mixer.music.load('assets/voices/dragon_success_voice.mp3')

    def frame(self, app, frame: tk.Frame):
        frame.grid()
        frame.pack()

        level = app.get_state('riddle')
        if level == 2:
            self.final_win(app=app, frame=frame)
        else:
            self.single_level_win(app=app, frame=frame)

    def single_level_win(self, app, frame):
        base_img = Image.open(self.base_img_path).resize((800, 800))
        overlay_image = Image.open(self.overlay_img_path).resize((400, 400))
        base_img.paste(overlay_image, (220, 300), overlay_image)
        combined_photo = ImageTk.PhotoImage(base_img)
        frame.photo = combined_photo
        self.dark_blue = app.theme['colors'].dark_blue
        self.btn_color = app.theme['colors'].btn_color
        self.success_color_purple = app.theme['colors'].success_color_purple
        self.error_color_pink = app.theme['colors'].error_color_pink
        self.title_font = app.theme['fonts'].hat_title_font

        canvas = tk.Canvas(frame, width=800, height=800)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=combined_photo, anchor='nw')

        back_icon = ImageTk.PhotoImage(Image.open(self.back_icon_path))
        frame.back_icon = back_icon
        back_btn = canvas.create_image(20, 20, image=back_icon)
        canvas.tag_bind(back_btn, "<Button-1>",
                        lambda event: app.push('dragon.home'))

        canvas.create_text(400, 200, text="Well down! Traveler!",
                font=app.theme['fonts'].dragon_default_font , anchor='center',
                           width=400, justify='center', fill='#A21F45')

    def final_win(self, app, frame):
        frame.grid()
        frame.pack()

        img = Image.open(self.final_win_path).resize((800, 800))
        photo = ImageTk.PhotoImage(img)
        frame.photo = photo

        canvas = tk.Canvas(frame, width=800, height=800)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=photo, anchor='nw')

        mixer.music.play()
        # frame.after(1, app.root.destroy())
        self.show_message(
                    frame, app, "RIGHT!", "You solved the puzzle!", self.error_color_pink)
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
