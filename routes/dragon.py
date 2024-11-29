from pages.dragon.home import DragonHomePage
from pages.dragon.riddle import DragonRiddlePage
from pages.dragon.win import DragonWinPage
from pages.dragon.game_over import DragonGameOverPage


def create_dragon_routes(router):
    router.add_route('dragon.home', DragonHomePage)
    router.add_route('dragon.riddle', DragonRiddlePage)
    router.add_route('dragon.win', DragonWinPage)
    router.add_route('dragon.game_over', DragonGameOverPage)
