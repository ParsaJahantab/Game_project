from PIL import Image, ImageTk
import tkinter as tk

from logics.dragon import DragonsLogic


class DragonRiddlePage:

    def __init__(self):
        self.riddle_bg_img_path = 'assets/images/riddle_background.png'
        self.riddles_path = 'assets/riddles/dragon/'
        self.submit_btn_img = ImageTk.PhotoImage(
            Image.open('assets/images/dragon_submit.png').resize((50, 50))
        )
        self.logic = DragonsLogic(self.riddles_path)

    def frame(self, app, frame: tk.Frame):
        frame.pack()

        msg = self.logic.riddles[app.get_state('riddle')]['riddle']

        img = Image.open(self.riddle_bg_img_path)
        img = img.resize((800, 800))
        photo = ImageTk.PhotoImage(img)

        frame.photo = photo

        canvas = tk.Canvas(frame, width=800, height=800)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=photo, anchor='nw')

        canvas.create_text(
            400, 200, text=msg, font=app.theme['fonts'].dragon_default_font, anchor='center', width=400, justify='center')

        self.answer_entry = tk.Entry(frame)
        canvas.create_window(400, 600, window=self.answer_entry)

        btn = canvas.create_image(400,  650, image=self.submit_btn_img)
        canvas.tag_bind(btn, "<Button-1>",
                        lambda event: self.submit_answer(app, frame))

    def submit_answer(self, app, frame):
        riddle_num = app.get_state('riddle')
        user_input = self.answer_entry.get()
        try:
            check_answer = self.logic.check_answer(
                user_input.lower(), riddle_num)
            app.set_state('solved', self.logic.solved_status())
            if check_answer:
                app.set_state(f'riddle{riddle_num}', True)
                app.push('dragon.win')
            else:
                app.push('dragon.game_over')
        except Exception as e:
            print(e)
            print('Invalid input')
