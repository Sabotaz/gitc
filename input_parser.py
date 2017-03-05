import config
from datatypes import *
import utils

config.FACTORY_COUNT = int(input())
config.LINK_COUNT = int(input())

def init_game():
    make_factories(config.FACTORY_COUNT)
    for i in range(config.LINK_COUNT):
        factory_1, factory_2, distance = map(int, input().split())
        add_factory_link(factory_1, factory_2, distance)
    utils.err(factory_links)
    
def init_loop():
    reset_attackers()
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        if entity_type == "FACTORY":
            update_factory(entity_id, int(arg_1), int(arg_2), int(arg_3), int(arg_4))
        elif entity_type == "TROOP":
            update_troop(entity_id, int(arg_1), int(arg_2), int(arg_3), int(arg_4), int(arg_5))
        elif entity_type == "BOMB":
            update_bomb(entity_id, int(arg_1), int(arg_2), int(arg_3), int(arg_4))
            