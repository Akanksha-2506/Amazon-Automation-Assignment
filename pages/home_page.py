"""
Amazon Home Page Object
-----------------------
Handles the landing page: cookie dismissal and the search bar.
"""

import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    # ── Selectors ─────────────────────────────────────────────────
    SEARCH_BOX    = "#twotabsearchtextbox"
    SEARCH_BUTTON = "#nav-search-submit-button"
    ACCEPT_COOKIE = "[data-cel-widget='sp-cc-accept'], #sp-cc-accept"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str) -> None:
        """Navigate to Amazon and dismiss any cookie banner."""
        self.navigate(base_url)
        self._dismiss_cookie_banner()

    def search(self, query: str) -> None:
        """Enter a search query and submit it."""
        logger.info("Searching for: %s", query)
        self.fill(self.SEARCH_BOX, query)
        self.click(self.SEARCH_BUTTON)

    # ── Private helpers ───────────────────────────────────────────
    def _dismiss_cookie_banner(self) -> None:
        try:
            btn = self.page.locator(self.ACCEPT_COOKIE)
            if btn.is_visible(timeout=3_000):
                btn.click()
                logger.info("Cookie banner dismissed.")
        except Exception:
            pass   # Banner not present — carry on
