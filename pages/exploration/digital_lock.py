from PIL import Image, ImageTk
import tkinter as tk

from logics.exploration import ExplorationLogic


class DigitalLockPage:

    def __init__(self):
        self.digital_lock_img = 'assets/images/electronic_lock.png'
        self.combinations_path = 'assets/safe_box/combination.json'
        self.back_icon_path = 'assets/images/arrow-left.png'
        self.hint_icon_path = 'assets/images/hint.png'
        self.comb_bg = 'assets/images/old_img.png'

        self.close_btn_img = ImageTk.PhotoImage(
            Image.open('assets/images/close2.png').resize((50, 50))
        )
        self.logic = ExplorationLogic(self.combinations_path)
        self.answer = ''

        self.text_id = None

    def frame(self, app, frame: tk.Frame):
        frame.pack()
        self.seven_segment = app.theme['fonts'].seven_segment

        self.title_font = app.theme['fonts'].hat_title_font
        self.btn_font = app.theme['fonts'].hat_btn_font
        self.input_font = app.theme['fonts'].hat_input_font
        self.default_font = app.theme['fonts'].hat_default_font

        self.btn_color = app.theme['colors'].btn_color
        self.success_color = app.theme['colors'].success_color
        self.error_color = app.theme['colors'].error_color

        img = Image.open(self.digital_lock_img)
        img = img.resize((800, 800))
        photo = ImageTk.PhotoImage(img)

        frame.photo = photo

        self.canvas = tk.Canvas(frame, width=800, height=800)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, image=photo, anchor='nw')

        back_icon = ImageTk.PhotoImage(Image.open(self.back_icon_path))
        frame.back_icon = back_icon
        back_btn = self.canvas.create_image(20, 20, image=back_icon)
        self.canvas.tag_bind(back_btn, "<Button-1>",
                             lambda event: app.push('exploration.home', key=app.get_state('key')))

        key = app.get_state('key')
        if key:
            hint_icon = ImageTk.PhotoImage(Image.open(
                self.hint_icon_path).resize((70, 70)))
            frame.hint_icon = hint_icon
            hint_btn = self.canvas.create_image(750, 750, image=hint_icon)
            self.canvas.tag_bind(hint_btn, "<Button-1>",
                                 lambda event: self.on_hint_click(frame))
        self.clickable_numbers(app, frame)

    def on_hint_click(self, frame):
        frame.grid()
        frame.pack()

        msg_box = tk.Toplevel(frame)
        msg_box.geometry("400x400")
        msg_box.title("Door's Combination")

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

    def add_clickable_area(self, app, frame, x1, y1, x2, y2, label):
        area = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="", fill="", width=2)
        self.canvas.tag_bind(area, "<Button-1>",
                             lambda event: self.on_click(app, frame, label))

    def clickable_numbers(self, app, frame):
        x0, y0 = 270, 210
        width = 60
        height = 60
        row_distance = 35
        col_distance = 40
        for i in range(3):
            y = y0 + i * (col_distance + height)
            for j in range(3):
                x = x0 + j * (row_distance + width)
                self.add_clickable_area(app, frame,
                                        x, y, x + width, y + height, str(i * 3 + j + 1))

        x = x0
        y = y0 + 3 * (col_distance + height)
        self.add_clickable_area(app, frame,
                                x, y, x + width, y + height, str('*'))
        x = x0 + (row_distance + width)
        self.add_clickable_area(app, frame,
                                x, y, x + width, y + height, str('0'))
        x = x0 + 2 * (row_distance + width)
        self.add_clickable_area(app, frame,
                                x, y, x + width, y + height, str('#'))

    def on_click(self, app, frame, label):
        if label == '#':
            self.answer_response(app, frame)
            self.answer = ''
            self.canvas.delete(self.text_id)
        else:
            self.answer += label

        if self.text_id is not None:
            self.canvas.delete(self.text_id)

        self.text_id = self.canvas.create_text(
            400, 600, text=self.answer, font=self.seven_segment, fill='blue', anchor='center', width=400, justify='center')

    def answer_response(self, app, frame):
        check_ans = self.logic.check_answer(self.answer)
        if check_ans:
            self.show_message(frame, app, 'Correct!',
                              'Congrats!!', self.success_color)
        elif self.logic.num_try == 3:
            self.show_message(frame, app, 'Wrong!',
                              'Wrong answer!!', self.error_color)
        else:
            self.canvas.create_text(
                400, 50, text='Wrong answer! Please try', font=app.theme['fonts'].dragon_default_font, fill='red', anchor='center', width=400, justify='center')

    def show_message(self, frame, app, title, message, color):
        frame.grid()
        frame.pack()

        msg_box = tk.Toplevel(frame)
        msg_box.geometry("300x150")
        msg_box.config(bg='#fff')
        msg_box.title(title)

        # Label for the message content with the custom font
        label = tk.Label(msg_box, text=message,
                         font=self.title_font, fg=color, bg='#fff')
        label.pack(pady=20)

        canvas = tk.Canvas(msg_box, width=300, height=100,
                           bg='#fff', highlightthickness=0)
        canvas.pack()
        close_btn = canvas.create_image(
            150, 50, image=self.close_btn_img, anchor='center')

        canvas.tag_bind(
            close_btn, "<Button-1>", lambda event: (msg_box.destroy(), app.root.quit()))
