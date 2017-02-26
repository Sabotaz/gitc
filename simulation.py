from datatypes import *
import config

def get_best_orders():
    mine = [i for i in range(config.FACTORY_COUNT) if factories[i][0] == 1]
    attackable_neutral_factories = []
    attackable_ennemy_factories = []
    for i in mine:
        if factories[i][1] > 0:
            possibles = [j for j in range(config.FACTORY_COUNT) if factory_links[i][j] != 0]
            for j in possibles:
                if factories[j][0] == 0:
                    attackable_neutral_factories += [(i,j)]
                if factories[j][0] == -1:
                    attackable_ennemy_factories += [(i,j)]
    
    orders = ["WAIT"]
    for i in mine:
        if factories[i][1] >= 10 and factories[i][2] < 3:
            orders += ["INC " + str(i)]
            factories[i][1] -= 10
    
    costs = []
            
    for i,j in attackable_neutral_factories + attackable_ennemy_factories:
        troops = factories[j][1]
        troops_respawn = factories[j][2] * factory_links[i][j]
        incomming = sum(incoming_troops[j])
        arriving = sum(arriving_troops[j])
        price_to_attack = troops + troops_respawn + incomming - arriving + 1
        if price_to_attack > 0:
            costs += [(i,j,price_to_attack)]
    
    costs.sort(key=lambda x: x[2])
    for i, j, cost in costs:
        if factories[i][1] >= cost:
            orders += ["MOVE " + str(i) + " " + str(j) + " " + str(cost)]
            factories[i][1] -= cost
        
        
    return orders