from pages.hat.home import HatsHomePage


def create_hat_routes(router):
    router.add_route('hat.home', HatsHomePage)
