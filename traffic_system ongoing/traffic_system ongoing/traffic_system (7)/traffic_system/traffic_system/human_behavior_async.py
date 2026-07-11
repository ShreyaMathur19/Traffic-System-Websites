import asyncio
import random


async def human_browse_async(page, duration):
    end_time = asyncio.get_event_loop().time() + duration

    while asyncio.get_event_loop().time() < end_time:
        try:
            await page.mouse.wheel(0, random.randint(200, 800))
            await asyncio.sleep(random.uniform(1.5, 3.5))
        except Exception:
            break