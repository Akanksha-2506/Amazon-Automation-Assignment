"""
Central configuration for test execution.
Supports both local Playwright and LambdaTest cloud execution.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Browser settings ──────────────────────────────────────────────
BROWSER = os.getenv("BROWSER", "chromium")   # chromium | firefox | webkit
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO  = int(os.getenv("SLOW_MO", "0"))    # ms delay between actions (0 = fastest)

# ── Timeouts (ms) ─────────────────────────────────────────────────
DEFAULT_TIMEOUT    = 30_000
NAVIGATION_TIMEOUT = 60_000

# ── URLs ──────────────────────────────────────────────────────────
BASE_URL = "https://www.amazon.com"

# ── Search keywords ───────────────────────────────────────────────
IPHONE_QUERY  = "Apple iPhone 15"
GALAXY_QUERY  = "Samsung Galaxy S24"

# ── LambdaTest credentials (set via .env or CI env vars) ──────────
LT_USERNAME    = os.getenv("LT_USERNAME", "")
LT_ACCESS_KEY  = os.getenv("LT_ACCESS_KEY", "")
LT_GRID_URL    = f"wss://cdp.lambdatest.com/playwright?capabilities="
USE_LAMBDATEST = bool(LT_USERNAME and LT_ACCESS_KEY)

# ── LambdaTest capability presets ────────────────────────────────
LT_CAPABILITIES = {
    "browserName": "Chrome",
    "browserVersion": "latest",
    "LT:Options": {
        "platform": "Windows 10",
        "build": "Amazon Automation Suite",
        "name": "Parallel Product Search Tests",
        "resolution": "1920x1080",
        "selenium_version": "4.0.0",
    },
}
