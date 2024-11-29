from routes.dragon import create_dragon_routes
from routes.hat import create_hat_routes
from routes.door import create_door_routes
from routes.matchstick import create_matchstick_routes
from routes.cannibal import create_cannibal_routes
from routes.exploration import create_exploration_routes


def create_routes(router):
    create_dragon_routes(router)
    create_hat_routes(router)
    create_door_routes(router)
    create_matchstick_routes(router)
    create_cannibal_routes(router)
    create_exploration_routes(router)