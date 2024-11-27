from puzzles.hats.hats_render import *
def hats():
        h = HatsPuzzleRenderer('./assets/images/hats.png', 2)
        h.render()
        return h.puzzle_status()