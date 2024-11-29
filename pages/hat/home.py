import tkinter as tk
from PIL import Image, ImageTk

from logics.hat import HatsLogic


class HatsHomePage:
    def __init__(self):
        correct_answer = 2
        self.image_path = 'assets/images/hats.png'
        self.logic = HatsLogic(correct_answer=correct_answer)

    def frame(self, app, frame: tk.Frame):
        frame.grid()
        frame.pack()

        self.white_color = app.theme['colors'].white_color
        self.btn_color = app.theme['colors'].btn_color
        self.success_color = app.theme['colors'].success_color
        self.error_color = app.theme['colors'].error_color

        self.title_font = app.theme['fonts'].hat_title_font
        self.btn_font = app.theme['fonts'].hat_btn_font
        self.input_font = app.theme['fonts'].hat_input_font

        app.update_title("Who can guess his hat's color right?")
        app.update_bg_color(self.white_color)
        frame.config(bg=self.white_color)

        # Load and display the image
        img = Image.open(self.image_path)
        img = img.resize((800, 400))
        photo = ImageTk.PhotoImage(img)

        # Create a label to display the image
        image_label = tk.Label(frame, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)

        # Create a label for the question with the custom font
        question_label = tk.Label(
            frame, text="Who guesses his hat color right?", bg=self.white_color, font=self.title_font)
        question_label.pack(pady=10)

        # Create an entry widget for the user input with the custom font
        self.answer_entry = tk.Entry(frame, font=self.input_font)
        self.answer_entry.pack(pady=10)

        # Create a submit button with the custom font
        submit_button = tk.Button(
            frame, text="Submit", font=self.btn_font, command=lambda: self.submit_answer(app, frame), bg=self.btn_color)
        submit_button.pack(pady=10)

    def submit_answer(self, app, frame):
        user_input = self.answer_entry.get()
        try:
            check_answer = self.logic.check_answer(int(user_input))
            app.set_state('solved', check_answer)
            if check_answer:
                self.show_message(frame, app,
                                  "Correct!", "You solved the puzzle!", self.success_color)
            else:
                self.show_message(
                    frame, app, "Wrong!", "You missed the puzzle!", self.error_color)
        except Exception:
            print('Invalid input')

    def show_message(self, frame, app, title, message, color):
        frame.grid()
        frame.pack()

        msg_box = tk.Toplevel(frame)
        msg_box.geometry("300x150")
        msg_box.config(bg=self.white_color)
        msg_box.title(title)

        # Label for the message content with the custom font
        label = tk.Label(msg_box, text=message,
                         font=self.title_font, fg=color, bg=self.white_color)
        label.pack(pady=20)

        # Create a button to close the message box with rounded corners
        close_button = tk.Button(
            msg_box, text="Close", font=self.btn_font, command=lambda: (msg_box.destroy(), app.root.destroy()), bg=self.btn_color)
        close_button.pack(pady=10)
