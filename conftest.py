"""
conftest.py
-----------
Shared pytest fixtures for browser lifecycle management.
Supports both local Playwright execution and LambdaTest cloud.
"""

import json
import logging
import urllib.parse
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from config.settings import (
    BROWSER, HEADLESS, SLOW_MO,
    DEFAULT_TIMEOUT, NAVIGATION_TIMEOUT,
    BASE_URL,
    USE_LAMBDATEST, LT_USERNAME, LT_ACCESS_KEY,
    LT_GRID_URL, LT_CAPABILITIES,
)

logger = logging.getLogger(__name__)


# ── Browser fixture (session-scoped for speed) ─────────────────────────────
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser_instance(playwright_instance):
    """
    Spin up a single browser process for the whole test session.
    Uses LambdaTest remote CDP if credentials are present.
    """
    if USE_LAMBDATEST:
        logger.info("Connecting to LambdaTest cloud…")
        caps = urllib.parse.quote(json.dumps(LT_CAPABILITIES))
        endpoint = f"{LT_GRID_URL}{caps}&user={LT_USERNAME}&accessKey={LT_ACCESS_KEY}"
        browser = playwright_instance.chromium.connect(endpoint)
    else:
        launch_fn = getattr(playwright_instance, BROWSER)
        browser = launch_fn.launch(headless=HEADLESS, slow_mo=SLOW_MO)

    yield browser
    browser.close()


# ── Context + Page fixtures (function-scoped = fresh per test) ─────────────
@pytest.fixture
def context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="America/New_York",
    )
    ctx.set_default_timeout(DEFAULT_TIMEOUT)
    ctx.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    pg = context.new_page()
    yield pg
    pg.close()


# ── Convenience fixture: base URL ──────────────────────────────────────────
@pytest.fixture
def base_url() -> str:
    return BASE_URL
