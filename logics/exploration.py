import json
import random


class ExplorationLogic:
    def __init__(self, path):
        self.path = path
        self.combination = self.read_from_file()
        self.num_try = 0
        self.solved = False

    def read_from_file(self):
        with open(self.path, 'r') as file:
            combinations = json.load(file)
        return random.choice(combinations)

    def check_answer(self, answer):
        if self.combination['answer'] == answer:
            self.solved = True
            return True
        self.num_try += 1
        return False

    def solved_status(self):
        return self.solved
