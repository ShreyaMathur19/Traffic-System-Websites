# click_behavior.py
import random
import time
from urllib.parse import urlparse

SAFE_SELECTORS = [
    "a[href]",
    "button",
    "[role=button]",
    "input[type=button]",
    "input[type=submit]",
    ".btn",
    ".cta",
    ".button",
    "article a",
    "main a",
]


def safe_randint(a, b):
    if a >= b:
        return a
    return random.randint(a, b)


def click_multiple_elements(page, max_clicks=12):
    clicks_done = 0
    start_time = time.time()
    MAX_DWELL_TIME = random.randint(20, 35)

    elements = []

    try:
        page.mouse.wheel(0, random.randint(200, 400))
        time.sleep(random.uniform(0.5, 1))
    except:
        pass

    for selector in SAFE_SELECTORS:
        try:
            elements.extend(page.query_selector_all(selector))
        except:
            pass

    valid_elements = []
    for el in elements:
        try:
            if not el.is_visible():
                continue
            box = el.bounding_box()
            if not box or box["y"] < 120:
                continue
            valid_elements.append(el)
        except:
            pass

    if len(valid_elements) < 3:
        return 0

    # ✅ CRITICAL FIX HERE
    min_clicks = min(4, len(valid_elements))
    max_clicks = min(max_clicks, len(valid_elements))

    clicks_target = safe_randint(min_clicks, max_clicks)

    used_elements = set()
    base_domain = urlparse(page.url).netloc.split(".", 1)[-1]

    for el in random.sample(valid_elements, clicks_target):

        if time.time() - start_time > MAX_DWELL_TIME:
            break

        try:
            if el in used_elements:
                continue

            href = el.get_attribute("href") or ""
            if href.startswith("http"):
                if not urlparse(href).netloc.endswith(base_domain):
                    continue

            url_before = page.url

            el.hover()
            time.sleep(random.uniform(0.3, 0.7))
            el.click(timeout=2500)

            used_elements.add(el)
            clicks_done += 1
            time.sleep(random.uniform(0.8, 1.5))

            if page.url != url_before:
                used_elements.clear()
                time.sleep(random.uniform(1.5, 2.5))
                page.mouse.wheel(0, random.randint(200, 400))

        except:
            continue

    return clicks_done
