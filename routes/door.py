from pages.door.home import DoorHomePage


def create_door_routes(router):
    router.add_route('door.home', DoorHomePage)
