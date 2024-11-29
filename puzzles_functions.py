from puzzles.hats.hats_render import *
from battleship import *
from core.app import App


def door():
    app = App("door.home", door="door0")
    app.set_state("solved", False)
    app.run()
    return app.get_state("solved")


def hats():
    app = App("hat.home")
    app.set_state("solved", False)
    app.run()
    return app.get_state("solved")


def battleship(g):
    game = BattleshipGame(g)
    return game.run()


def dragons():
    app = App("dragon.home")
    app.set_state("solved", False)
    app.run()
    return app.get_state("solved")


def matchstick():
    app = App("matchstick.home")
    app.set_state("solved", False)
    app.run()
    return app.get_state("solved")
