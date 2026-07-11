import random
import asyncio

async def click_multiple_elements_async(page, max_clicks=6):
    try:
        elements = await page.query_selector_all("a[href], button")
    except:
        return 0

    if not elements:
        return 0

    random.shuffle(elements)
    clicks = 0

    for el in elements[:max_clicks]:
        try:
            await el.hover()
            await asyncio.sleep(random.uniform(0.3, 0.8))
            await el.click(timeout=2000)
            clicks += 1
            await asyncio.sleep(random.uniform(1, 2))
        except:
            continue

    return clicks
