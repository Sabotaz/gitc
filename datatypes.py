import config
import utils

factories = []
factory_links = None
incoming_troops = []
arriving_troops = []
bombs = 2
score = 0
my_bombs = []
ennemies_bombs = []
ennemies_bombs_history = dict()
first_spawn = None

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
    global incoming_troops, arriving_troops, my_bombs, ennemies_bombs, score, first_spawn
    incoming_troops = [[0]*20 for _ in range(config.FACTORY_COUNT)]
    arriving_troops = [[0]*20 for _ in range(config.FACTORY_COUNT)]
    if not ennemies_bombs:
        first_spawn = -1
    my_bombs = []
    ennemies_bombs = []
    score = 0

def update_factory(entity_id, player, cyborgs, prod, freeze):
    global first_spawn
    factories[entity_id][0] = player
    factories[entity_id][1] = cyborgs
    factories[entity_id][2] = prod
    factories[entity_id][3] = freeze
    if player == 1:
        global score
        score += cyborgs
        if not first_spawn:
            first_spawn = entity_id


def update_bomb(entity_id, player, start, end, tours):
    global my_bombs, ennemies_bombs, ennemies_bombs_history
    if player == 1:
        my_bombs += [[start, end, tours]]
    else:
        if entity_id not in ennemies_bombs_history:
            ennemies_bombs_history[entity_id] = 0
        else:
            ennemies_bombs_history[entity_id] = ennemies_bombs_history[entity_id] + 1
        ennemies_bombs += [[start, ennemies_bombs_history[entity_id]]]

def update_troop(entity_id, player, start, end, size, tours):
    if player == 1:
        arriving_troops[end][tours-1] += size
        global score
        score += size
    else:
        incoming_troops[end][tours-1] += size
        
