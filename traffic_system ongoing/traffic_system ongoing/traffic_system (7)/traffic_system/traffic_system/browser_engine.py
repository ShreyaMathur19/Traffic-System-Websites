# browser_engine.py
import time
import uuid
import random

from config import HEADLESS
from human_behavior import human_browse
from click_behavior import click_multiple_elements
from excel_logger import log_session


def get_public_ip(page):
    try:
        page.goto("https://api.ipify.org", timeout=15000)
        ip = page.text_content("body")
        return ip.strip() if ip else None
    except:
        return None


def visit_site(
    playwright,
    google_referrer,
    times_url,
    genpulse_url,
    duration,
    device,
    behavior=None,
):
    session_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    total_clicks = 0
    status = "SUCCESS"
    error_reason = None
    ip = None

    context = None
    browser = None

    try:
        browser = playwright.chromium.launch(headless=False)

        context = browser.new_context(
            viewport=device["viewport"],
            user_agent=device["user_agent"],
            is_mobile=device["is_mobile"],
            has_touch=device["has_touch"],
            locale="en-IN",
            timezone_id="Asia/Kolkata",
        )

        # ---------- TAB 1: TIMES OF INDIA ----------
        page_times = context.new_page()
        page_times.goto(
            times_url,
            referer=google_referrer,
            wait_until="networkidle",
            timeout=60000,
        )

        # Scroll + interact TOI
        page_times.mouse.wheel(0, 1200)
        time.sleep(2)
        total_clicks += human_browse(page_times, device)

        # ---------- TAB 2: GENPULSE ----------
        page_genpulse = context.new_page()
        page_genpulse.goto(
            genpulse_url,
            referer=google_referrer,
            wait_until="networkidle",
            timeout=60000,
        )

        # Scroll + interact GenPulse
        page_genpulse.mouse.wheel(0, 1200)
        time.sleep(2)

        if behavior:
            total_clicks += behavior(page_genpulse)
        else:
            total_clicks += click_multiple_elements(page_genpulse)

        # 🔁 Switch back to TOI once more
        page_times.bring_to_front()
        page_times.mouse.wheel(0, 800)
        time.sleep(2)

        time.sleep(min(duration, random.randint(10, 15)))

    except Exception as e:
        status = "FAIL"
        error_reason = str(e)
        print(f"[ERROR] {session_id} -> {error_reason}")

    finally:
        if context:
            context.close()
        if browser:
            browser.close()

    log_session(
        session_id=session_id,
        referrer=google_referrer,
        destination=genpulse_url,
        device_type=device["name"],
        total_time=int(time.time() - start_time),
        click_count=total_clicks,
        ip=ip,
        proxy=None,
        city=None,
        status=status,
        error_reason=error_reason,
    )

    print(f"[DONE] {session_id} | {status} | clicks={total_clicks}")
