# devices.py

DESKTOP = {
    "name": "desktop",
    "viewport": {"width": 1366, "height": 768},
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "is_mobile": False,
    "has_touch": False,
}

MOBILE = {
    "name": "mobile",
    "viewport": {"width": 390, "height": 844},
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "is_mobile": True,
    "has_touch": True,
}
