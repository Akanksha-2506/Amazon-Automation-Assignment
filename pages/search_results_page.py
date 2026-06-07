"""
Search Results Page Object
--------------------------
Picks the first eligible (in-stock, non-sponsored) result and
navigates to its product detail page.
"""

import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class SearchResultsPage(BasePage):
    # ── Selectors ─────────────────────────────────────────────────
    # Each result card
    RESULT_ITEMS = "div[data-component-type='s-search-result']"
    # Title link inside a result card
    TITLE_LINK   = "h2 a.a-link-normal"
    # Price whole + fraction
    PRICE_WHOLE  = ".a-price-whole"

    def __init__(self, page: Page):
        super().__init__(page)

    def open_first_result(self) -> str:
        """
        Click the first product result.
        Returns the product title text for logging purposes.
        """
        logger.info("Waiting for search results…")
        self.page.wait_for_selector(self.RESULT_ITEMS, timeout=30_000)

        # Grab the first result card and extract its title link
        first_card = self.page.locator(self.RESULT_ITEMS).first
        title_link  = first_card.locator(self.TITLE_LINK).first
        title_text  = title_link.inner_text().strip()

        logger.info("Opening product: %s", title_text)
        title_link.click()
        return title_text
