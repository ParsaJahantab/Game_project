from pages.exploration.digital_lock import DigitalLockPage
from pages.exploration.home import ExplorationHomePage


def create_exploration_routes(router):
    router.add_route('exploration.home', ExplorationHomePage)
    router.add_route('exploration.digital_lock', DigitalLockPage)
