# human_behavior.py
import time
import random

def human_browse(page, device):
    clicks = 0

    try:
        elements = page.query_selector_all("a[href]")
    except:
        return 0

    max_clicks = random.randint(1, 2)

    for el in elements[:max_clicks]:
        try:
            el.hover()
            time.sleep(random.uniform(0.3, 0.6))
            el.click(timeout=2000)
            clicks += 1
            time.sleep(random.uniform(0.8, 1.4))
        except:
            pass

    return clicks
