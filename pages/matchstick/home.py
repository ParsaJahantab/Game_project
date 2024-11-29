import tkinter as tk
from PIL import Image, ImageTk

from logics.matchstick import MatchstickLogic


class MatchstickHomePage:
    def __init__(self):
        self.image_bg_path = 'assets/images/matchstick_bg3.png'
        self.equations_path = 'assets/matchstick/matchstick.json'
        self.submit_btn_img = ImageTk.PhotoImage(
            Image.open('assets/images/light_submit.png').resize((50, 50))
        )
        self.close_btn_img = ImageTk.PhotoImage(
            Image.open('assets/images/close.png').resize((50, 50)))

        self.logic = MatchstickLogic(path=self.equations_path)

    def frame(self, app, frame: tk.Frame):
        frame.grid()
        frame.pack()

        self.dark_blue = app.theme['colors'].dark_blue
        self.btn_color = app.theme['colors'].btn_color
        self.success_color_purple = app.theme['colors'].success_color_purple
        self.error_color_pink = app.theme['colors'].error_color_pink

        self.seven_segment_font = app.theme['fonts'].seven_segment
        self.title_font = app.theme['fonts'].hat_title_font
        self.btn_font = app.theme['fonts'].hat_btn_font
        self.input_font = app.theme['fonts'].hat_input_font
        self.default_font = app.theme['fonts'].hat_default_font

        app.update_title("What Is the Correct Equation?")

        # Load and display the image
        img = Image.open(self.image_bg_path)
        img = img.resize((800, 800))
        photo = ImageTk.PhotoImage(img)
        frame.photo = photo

        canvas = tk.Canvas(frame, width=800, height=800)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=photo, anchor='nw')

        canvas.create_text(
            400, 200, text='Fix the equation by replacing a single matchstick!!', font=self.default_font, fill='yellow', anchor='center', width=400, justify='center')
        canvas.create_text(
            400, 400, text=self.logic.equation['equation'], font=self.seven_segment_font, fill='yellow', anchor='center', width=400, justify='center')

        self.answer_entry = tk.Entry(frame)
        canvas.create_window(400, 500, window=self.answer_entry)

        btn = canvas.create_image(400,  550, image=self.submit_btn_img)
        canvas.tag_bind(btn, "<Button-1>",
                             lambda event: self.submit_answer(app, frame))

    def submit_answer(self, app, frame):
        user_input = self.answer_entry.get()
        user_input = user_input.replace(' ', '')
        try:
            check_answer = self.logic.check_answer(user_input.lower())
            app.set_state('solved', self.logic.solved_status())
            if check_answer:
                self.show_message(frame, app,
                                  "Correct!", "You solved the puzzle!", self.success_color_purple)
            else:
                self.show_message(
                    frame, app, "Wrong!", "You missed the puzzle!", self.error_color_pink)
        except Exception as e:
            print(e)
            print('Invalid input')

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
