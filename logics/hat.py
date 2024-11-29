class HatsLogic:
    def __init__(self, correct_answer):
        self.correct_answer = correct_answer
        self.solved = False

    def check_answer(self, answer):
        if self.correct_answer == answer:
            self.solved = True
        return self.solved

    def solved_status(self):
        return self.solved
