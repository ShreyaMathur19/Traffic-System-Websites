import asyncio
import time
import uuid
import random

from human_behavior_async import human_browse_async
from excel_logger import log_session


async def run_tab(page, url, referrer, duration):
    try:
        await page.goto(
            url,
            referer=referrer,
            wait_until="domcontentloaded",
            timeout=60000,
        )
        await human_browse_async(page, duration)

    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"[WARN] Tab failed: {url} -> {e}")


async def visit_site_async(
    browser,
    referrer,
    destination_urls,
    duration,
    device,
):
    session_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    context = await browser.new_context(
        viewport=device["viewport"],
        user_agent=device["user_agent"],
        is_mobile=device["is_mobile"],
        has_touch=device["has_touch"],
        locale="en-IN",
        timezone_id="Asia/Kolkata",
    )

    # 1️⃣ OPEN GOOGLE (REFERRER) FIRST
    ref_page = await context.new_page()
    try:
        await ref_page.goto(
            referrer,
            wait_until="domcontentloaded",
            timeout=60000,
        )
        await human_browse_async(ref_page, random.randint(5, 10))
    except Exception as e:
        print(f"[WARN] Referrer failed: {referrer} -> {e}")

    # 2️⃣ OPEN DESTINATION URLS IN PARALLEL TABS
    tasks = []
    for url in destination_urls:
        page = await context.new_page()
        tasks.append(
            asyncio.create_task(
                run_tab(page, url, referrer, duration)
            )
        )

    # 3️⃣ WAIT FOR ALL TABS
    await asyncio.gather(*tasks, return_exceptions=True)

    await context.close()

    total_time = int(time.time() - start_time)

    log_session(
        session_id=session_id,
        referrer=referrer,
        destination=" | ".join(destination_urls),
        device_type=device["name"],
        total_time=total_time,
        click_count=0,
        ip=None,
        proxy=None,
        city=None,
        status="SUCCESS",
        error_reason=None,
    )

    print(f"[DONE] {session_id} | {total_time}s | {len(destination_urls)} tabs")