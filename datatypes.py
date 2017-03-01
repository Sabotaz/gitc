import config
import utils

factories = []
factory_links = None
incoming_troops = []
arriving_troops = []
minimal_path = []

def make_factories(factory_count):
    global factories, factory_links, incoming_troops, arriving_troops, minimal_path
    factories = [[0,0,0,0] for _ in range(factory_count)]
    factory_links = [[0]*factory_count for _ in range(factory_count)]
    minimal_path = [[[] for _ in range(factory_count)] for _ in range(factory_count)]
    incoming_troops = [[0]*20 for _ in range(factory_count)]
    arriving_troops = [[0]*20 for _ in range(factory_count)]

def add_factory_link(factory_1, factory_2, distance):
    factory_links[factory_1][factory_2] = distance
    factory_links[factory_2][factory_1] = distance

def reset_attackers():
    global incoming_troops, arriving_troops
    incoming_troops = [[0]*20 for _ in range(config.FACTORY_COUNT)]
    arriving_troops = [[0]*20 for _ in range(config.FACTORY_COUNT)]

def update_factory(entity_id, player, cyborgs, prod, freeze):
    factories[entity_id][0] = player
    factories[entity_id][1] = cyborgs
    factories[entity_id][2] = prod
    factories[entity_id][3] = freeze

def update_bomb(entity_id, player, start, end, tours):
    pass

def update_troop(entity_id, player, start, end, size, tours):
    if player == 1:
        arriving_troops[end][tours] += size
    else:
        incoming_troops[end][tours] += size
        