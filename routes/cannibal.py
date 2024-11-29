from pages.cannibal.home import CannibalHomePage


def create_cannibal_routes(router):
    router.add_route('cannibal.home', CannibalHomePage)
