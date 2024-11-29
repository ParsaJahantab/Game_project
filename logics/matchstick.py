import json
import random


class MatchstickLogic:
    def __init__(self, path):
        self.path = path
        self.equation = self.read_from_file()
        self.solved = False

    def read_from_file(self):
        with open(self.path, 'r') as file:
            equations = json.load(file)
        return random.choice(equations)

    def check_answer(self, answer):
        if self.equation['answer'] == answer:
            self.solved = True
            return True
        return False

    def solved_status(self):
        return self.solved
