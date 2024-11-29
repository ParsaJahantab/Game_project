import json
import random


class DragonsLogic:
    def __init__(self, path):
        self.riddle_paths = path
        self.riddles = self.read_from_file()
        self.solved = False

    def read_from_file(self):
        riddle_types = ['easy', 'normal', 'hard']
        final_riddles = []
        for riddle in riddle_types:
            path = f'{self.riddle_paths}{riddle}.json'
            with open(path, 'r') as file:
                riddles = json.load(file)
            idx = self.random_riddle(len(riddles))
            final_riddles.append(riddles[idx])
        return final_riddles

    def random_riddle(self, n):
        riddle_idx = random.randint(0, n - 1)
        return riddle_idx

    def check_answer(self, answer, riddle_num):
        if riddle_num == 2 and self.riddles[riddle_num]['answer'] == answer:
            self.solved = True
            return True
        if self.riddles[riddle_num]['answer'] == answer:
            return True
        return False

    def solved_status(self):
        return self.solved
