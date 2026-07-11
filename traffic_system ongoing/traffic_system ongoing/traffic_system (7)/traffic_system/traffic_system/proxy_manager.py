# proxy_manager.py

import random
from config import LOCATIONS

def get_random_location():
    return random.choice(LOCATIONS)
