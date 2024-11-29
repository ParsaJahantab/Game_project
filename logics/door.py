import json


class DoorLogic:
    def __init__(self, path, door):
        self.path = path
        self.door_riddle = self.read_from_file(door=door)
        self.solved = False

    def read_from_file(self, door):
        with open(self.path, 'r') as file:
            riddle = json.load(file)
        return riddle[door]

    def check_answer(self, answer):
        if self.door_riddle['answer'] == answer:
            self.solved = True
            return True
        return False

    def solved_status(self):
        return self.solved
