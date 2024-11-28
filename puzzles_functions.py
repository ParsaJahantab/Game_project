from puzzles.hats.hats_render import *
from battleship import *


def hats():
    h = HatsPuzzleRenderer("./assets/images/hats.png", 2)
    h.render()
    return h.puzzle_status()


def battleship(g):
    game = BattleshipGame(g)
    return game.run()
