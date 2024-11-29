from pages.matchstick.home import MatchstickHomePage


def create_matchstick_routes(router):
    router.add_route('matchstick.home', MatchstickHomePage)
