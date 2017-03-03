import sys
import math
from datatypes import *
from utils import *
from input_parser import *
from simulation import *
import config

init_game()

# game loop
loop = 0
while True:
    t = current_micro_time()
    init_loop()
    
    order = get_best_orders()
        
    bomb_order, bombing_score = get_bomb_now()
    if bombs > 0 and bombing_score > 14:
        order += bomb_order
        bombs -= 1
        
    micro = current_micro_time() - t
    ms = (micro // 100) / 10
    
    messages = []
    messages += [str(ms) + "ms"]
    messages += ["bomb: " + str(bombing_score)]
    
    order += ["MSG " + ", ".join(messages)]
    
    print(";".join(order))
    loop += 1
