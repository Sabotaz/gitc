import sys
import math
from datatypes import *
from utils import *
from input_parser import *
from simulation import *
import config

init_game()

# game loop
while True:
    init_loop()
    
    order = get_best_orders()
    print(";".join(order))
