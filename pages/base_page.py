"""
Base Page Object
----------------
All page objects inherit from BasePage so common browser interactions
(wait, click, fill, screenshot) are defined in one place.
"""

import logging
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ── Navigation ────────────────────────────────────────────────
    def navigate(self, url: str) -> None:
        logger.info("Navigating to: %s", url)
        self.page.goto(url, wait_until="domcontentloaded")

    # ── Element helpers ───────────────────────────────────────────
    def click(self, selector: str, timeout: int = 30_000) -> None:
        logger.info("Clicking: %s", selector)
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str) -> None:
        logger.info("Filling '%s' into: %s", text, selector)
        self.page.locator(selector).fill(text)

    def get_text(self, selector: str, timeout: int = 30_000) -> str:
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    # ── Screenshot helper ─────────────────────────────────────────
    def screenshot(self, name: str) -> None:
        path = f"reports/{name}.png"
        self.page.screenshot(path=path, full_page=False)
        logger.info("Screenshot saved: %s", path)
