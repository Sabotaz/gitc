from datatypes import *
import config

def interest(j): # is it interesting to attack this city
    coef_neutral = 5
    coef_prod = 1
    coef_position_ennemies = 1
    coef_position_allies = 2
    coef_position = 0.1
    
    position_bonus = 0 # is it more close to allies than to ennemies
    pos_ennemies = 0
    ennemies = 0
    pos_allies = 0
    allies = 0
    for i in range(config.FACTORY_COUNT):
        if i != j:
            if factories[i][0] == 1:
                pos_allies += factory_links[i][j]
                allies += 1
            elif factories[i][0] == -1:
                pos_ennemies += factory_links[i][j]
                ennemies += 1
    #position_bonus = (pos_allies / allies)# - (pos_ennemies / ennemies)
    position_bonus_ennemies = (pos_ennemies / ennemies) if ennemies > 0 else 20
    position_bonus_allies = (20 - pos_allies / allies) if allies > 0 else 0
    position_bonus = coef_position_ennemies * position_bonus_ennemies + coef_position_allies * position_bonus_allies
    return coef_neutral * (factories[j][0] == 0) + coef_prod * factories[j][2] + int(coef_position * position_bonus)
    
def defences(j):
    troops = factories[j][1]
    min_ennemy_link = 20
    for i in range(config.FACTORY_COUNT):
        if i != j:
            if factories[i][0] == -1:
                min_ennemy_link = min(min_ennemy_link,factory_links[i][j])
    
    troops_respawn = factories[j][2] * min_ennemy_link
    
    incomming = sum(incoming_troops[j])
    arriving = sum(arriving_troops[j])
    
    defence = troops + troops_respawn + arriving - incomming -1
    
    return defence
    
def is_it_safe_to_inc(j):
    return defences(j) > 10

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
        if factories[i][2] < 3 and factories[i][1] >= 10 and (is_it_safe_to_inc(i) or factories[i][2] == 0):
            orders += ["INC " + str(i)]
            factories[i][1] -= 10
    
    costs = []
            
    for i,j in attackable_neutral_factories + attackable_ennemy_factories:
        troops = factories[j][1]
        troops_respawn = factories[j][2] * factory_links[i][j]
        incomming = sum(incoming_troops[j])
        arriving = sum(arriving_troops[j])
        price_to_attack = troops + troops_respawn + incomming - arriving + 1 + 10*(factories[j][2]==0)
        if price_to_attack > 0:
            costs += [(i,j,price_to_attack)]
    
    costs.sort(key=lambda x: (interest(x[1]),x[2]), reverse=True)
    for i, j, cost in costs:
        if factories[i][1] >= cost:
            orders += ["MOVE " + str(i) + " " + str(j) + " " + str(cost)]
            factories[i][1] -= cost
        
        
    return orders
