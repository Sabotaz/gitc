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
        
    micro = current_micro_time() - t
    ms = (micro // 100) / 10
    
    messages = []
    messages += [str(ms) + "ms"]
    
    order += ["MSG " + ", ".join(messages)]
    
    print(";".join(order))
    loop += 1
