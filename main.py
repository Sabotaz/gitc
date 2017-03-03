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
    init_loop()
    
    order = get_best_orders()
    bomb_order, bombing_score = get_bomb_now()
    err("bombing score: ", bombing_score)
    if bombs > 0 and (bombing_score > 20 or loop == 0):
        order += bomb_order
        bombs -= 1
        
    print(";".join(order))
    loop += 1
