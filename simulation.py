from datatypes import *
import config
import utils

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
    
def estimate_fights(j): # positive:ally  -  negative:ennemie
    player = factories[j][0]
    troops = factories[j][1]
    neutral = False
    if player != 0:
        troops *= player
    else:
        neutral = True
    
    for t in range(20):
        if player == -1:
            troops -= factories[j][2]
        elif player == 1:
            troops += factories[j][2]
        combat = arriving_troops[j][t] - incoming_troops[j][t]
        if neutral:
            troops -= abs(combat)
            if troops < 0:
                neutral = False
                if combat > 0: # c'est moi qui ai gagne
                    troops = abs(troops)
        else:
            troops += combat
        
        if troops > 0 and not neutral:
            player = 1
        if troops < 0 and not neutral:
            player = -1
    return abs(troops), player

def bombing_interest(ij):
    i, j = ij
    coef_prod = 3
    coef_troops = 0.2
    coef_multiple = 1
    coef_dist = 0.3
    
    troops = coef_troops * factories[j][1]
    prod = coef_prod * factories[j][2]
    count = 0
    for k in range(config.FACTORY_COUNT):
        if factory_links[i][k] == factory_links[i][j]:
            count += 1
    count *= coef_multiple
    dist = (20 - factory_links[i][j]) * coef_dist
    
    return troops + prod + count + dist

def get_bomb_now():
    mine = [i for i in range(config.FACTORY_COUNT) if factories[i][0] == 1]
    ennemies = [i for i in range(config.FACTORY_COUNT) if factories[i][0] == -1]
    bombing = []
    for i in mine:
        for j in ennemies:
            bombing += [(i,j)]
    bombing.sort(key=bombing_interest)
    i, j = bombing[-1]
    bombing_score = bombing_interest((i, j))
    return ["BOMB " + str(i) + " " + str(j)], bombing_score

def get_best_orders():
    mine = [i for i in range(config.FACTORY_COUNT) if factories[i][0] == 1]
    attackable_neutral_factories = []
    attackable_ennemy_factories = []
    defendable_allies_factories = []
    
    for i in mine:
        for i2 in mine:
            if i2 != i:
                estimation, player = estimate_fights(i)
                if player != 1:
                    defendable_allies_factories += [(i2,i)]
    
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
        if factories[i][2] < 3 and factories[i][1] >= 10 and is_it_safe_to_inc(i):
            orders += ["INC " + str(i)]
            factories[i][1] -= 10
    
    costs = []
            
    for i,j in attackable_neutral_factories + attackable_ennemy_factories + defendable_allies_factories:
        troops = factories[j][1]
        estimation, player = estimate_fights(j)
        if player != 1:
            troops_respawn = factories[j][2] * (factory_links[i][j] + 1) if factories[j][0]!=0 else 0
            incomming = sum(incoming_troops[j])
            arriving = sum(arriving_troops[j])
            price_to_attack = troops + troops_respawn + incomming - arriving + 1 + 10*(factories[j][2]==0)
            if price_to_attack > 0:
                costs += [(i,j,price_to_attack)]
    
    costs.sort(key=lambda x: (interest(x[1]),x[2]), reverse=True)
    attacked = set()
    for i, j, cost in costs:
        if factories[i][1] >= cost and j not in attacked:
            orders += ["MOVE " + str(i) + " " + str(j) + " " + str(cost)]
            factories[i][1] -= cost
            attacked.add(j)
        
        
    return orders
