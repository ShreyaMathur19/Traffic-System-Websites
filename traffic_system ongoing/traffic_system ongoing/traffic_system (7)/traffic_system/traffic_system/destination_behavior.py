# destination_behavior.py
from click_behavior import click_multiple_elements
import time
import random


def safe_randint(a, b):
    if a >= b:
        return a
    return random.randint(a, b)


def destination_browse(page):
    clicks = 0

    # Initial pause (FAST mode)
    time.sleep(random.uniform(2, 4))

    # Human-like scrolling (SAFE)
    for _ in range(safe_randint(2, 4)):
        page.mouse.wheel(0, random.randint(400, 900))
        time.sleep(random.uniform(1, 2))

    # First batch of clicks (SAFE)
    performed = click_multiple_elements(
        page,
        max_clicks=safe_randint(3, 5)
    )
    clicks += performed

    # Pause after interactions
    time.sleep(random.uniform(2, 4))

    # Another scroll
    page.mouse.wheel(0, random.randint(600, 1200))
    time.sleep(random.uniform(1.5, 3))

    # Second batch of clicks (SAFE)
    performed = click_multiple_elements(
        page,
        max_clicks=safe_randint(2, 4)
    )
    clicks += performed

    return clicks
