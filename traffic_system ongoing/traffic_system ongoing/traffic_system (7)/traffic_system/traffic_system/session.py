import asyncio
import random
from playwright.async_api import async_playwright

from browser_engine_async import visit_site_async
from devices import DESKTOP, MOBILE
from config import (
    DESTINATION_URLS,
    DELAY_BETWEEN_SESSIONS,
    GOOGLE_REFERRER,
)

MOBILE_RATIO = 0.6
SESSION_DURATION = 60  # ✅ exactly 1 minute


def pick_device():
    return MOBILE if random.random() < MOBILE_RATIO else DESKTOP


async def start_session_async(parallel=3):
    cycle = 0

    async with async_playwright() as p:
        while True:
            cycle += 1
            print("=" * 60)
            print(f"[CYCLE {cycle}] Starting Google sessions")

            browser = await p.chromium.launch(headless=False)
            sem = asyncio.Semaphore(parallel)

            async def run():
                async with sem:
                    await visit_site_async(
                        browser=browser,
                        referrer=GOOGLE_REFERRER,          # ✅ Google only
                        destination_urls=DESTINATION_URLS,
                        duration=SESSION_DURATION,        # ✅ fixed 60s
                        device=pick_device(),
                    )

            # Run N parallel sessions
            await asyncio.gather(*(run() for _ in range(parallel)))

            await browser.close()

            delay = random.uniform(*DELAY_BETWEEN_SESSIONS)
            print(f"[WAIT] Sleeping {delay:.2f}s")
            await asyncio.sleep(delay)