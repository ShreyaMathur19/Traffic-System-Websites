# behavior.py
import time
import random
from config import DWELL_TIME_SECONDS

def human_behavior(page):
    stay_time = random.randint(
        DWELL_TIME_SECONDS["min"],
        DWELL_TIME_SECONDS["max"]
    )

    try:
        page.mouse.wheel(0, random.randint(200, 800))
    except:
        pass

    time.sleep(stay_time)
