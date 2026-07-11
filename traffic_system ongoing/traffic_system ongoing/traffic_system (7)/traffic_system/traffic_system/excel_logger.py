# excel_logger.py
import os
import csv
from datetime import datetime
from multiprocessing import Lock

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

_csv_lock = Lock()

HEADERS = [
    "Timestamp",
    "Session ID",
    "Referrer",
    "Destination",
    "Device Type",
    "Total Time (seconds)",
    "Clicks",
    "IP",
    "City",
    "Proxy",
    "Status",
    "Error Reason"
]

def _get_today_csv():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"traffic_{today}.csv")


def log_session(
    session_id,
    referrer,
    destination,
    device_type,
    total_time,
    click_count,
    ip=None,
    proxy=None,
    city=None,
    status="SUCCESS",
    error_reason=None
):
    logfile = _get_today_csv()
    file_exists = os.path.exists(logfile)

    with _csv_lock:
        with open(logfile, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(HEADERS)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                session_id,
                referrer,
                destination,
                device_type,
                total_time,
                click_count,
                ip,
                city,
                proxy,
                status,
                error_reason
            ])
