import tkinter as tk
import tkinter.font as tkFont
from tkinter import font
from PIL import Image, ImageTk  # Use Pillow for image handling
from puzzles.hats.hats_logic import HatsLogic

from settings import *


class HatsPuzzleRenderer:
    def __init__(self, image_path, correct_answer):
        self.image_path = image_path
        self.logic = HatsLogic(correct_answer=correct_answer)

        # Root window will be initialized later
        self.root = None

    def render(self):
        # Create a Tkinter root window
        self.root = tk.Tk()
        self.root.title("Who can guess his hat's color right?")
        # self.defaultFont = font.nametofont("TKDefaultFont")
        # self.defaultFont.configure(family="Blomberg", weight=font.BOLD, size=20)
        
        self.defaultFont = tkFont.Font(family="Blomberg", weight=font.BOLD, size=20)
        self.titleFont = tkFont.Font(family="Blomberg", weight=font.BOLD, size=20)
        self.btnFont = tkFont.Font(family="Blomberg", size=16)
        self.inputFont = tkFont.Font(family="Blomberg", size=16)

        # Set window size
        self.root.geometry("500x500")
        self.root.config(bg=white_color)

        # Load and display the image
        img = Image.open(self.image_path)
        photo = ImageTk.PhotoImage(img)

        # Create a label to display the image
        image_label = tk.Label(self.root, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)

        # Create a label for the question with the custom font
        question_label = tk.Label(
            self.root, text="Who guesses his hat color right?", bg=white_color, font=self.titleFont)
        question_label.pack(pady=10)

        # Create an entry widget for the user input with the custom font
        self.answer_entry = tk.Entry(self.root, font=self.inputFont)
        self.answer_entry.pack(pady=10)

        # Create a submit button with the custom font
        submit_button = tk.Button(
            self.root, text="Submit", font=self.btnFont, command=self.submit_answer, bg=btn_color)
        submit_button.pack(pady=10)

        # Keep the window open until the answer is submitted
        self.root.mainloop()

    def submit_answer(self):
        user_input = self.answer_entry.get()
        if self.logic.check_answer(int(user_input)):
            self.show_message("Correct!", "You solved the puzzle!", success_color)
        else:
            self.show_message("Wrong!", "You missed the puzzle!", error_color)

    def show_message(self, title, message, color):
        # Create a custom message box to match the dialog design
        msg_box = tk.Toplevel(self.root)
        msg_box.geometry("300x150")
        msg_box.config(bg=white_color)
        msg_box.title(title)

        # Label for the message content with the custom font
        label = tk.Label(msg_box, text=message,
                         font=self.titleFont, fg=color, bg=white_color)
        label.pack(pady=20)

        # Create a button to close the message box with rounded corners
        close_button = tk.Button(
            msg_box, text="Close", font=self.btnFont, command=lambda: (msg_box.destroy(), self.root.destroy()), bg=btn_color)
        close_button.pack(pady=10)

    def puzzle_status(self):
        return self.logic.solved_status()


