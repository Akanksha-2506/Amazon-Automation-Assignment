"""
Product Detail Page Object
--------------------------
Extracts price, handles variant selection, and adds item to cart.
"""

import logging
import re
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    # ── Selectors ─────────────────────────────────────────────────
    ADD_TO_CART_BTN   = "#add-to-cart-button"
    PRODUCT_TITLE     = "#productTitle"

    # Price — Amazon renders prices in several different DOM structures
    PRICE_SELECTORS = [
        "#corePriceDisplay_desktop_feature_div .a-price-whole",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        ".a-price .a-offscreen",
        "#price_inside_buybox",
        "#kindle-price",
    ]

    CART_CONFIRM = "#NATC_SMART_WAGON_CONF_MSG_SUCCESS, #huc-v2-order-row-confirm-text"

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Public API ────────────────────────────────────────────────
    def get_price(self) -> str:
        """
        Try multiple selectors to extract the product price.
        Returns a formatted price string e.g. '$799.99'.
        """
        self.page.wait_for_load_state("domcontentloaded")

        for selector in self.PRICE_SELECTORS:
            try:
                locator = self.page.locator(selector).first
                if locator.is_visible(timeout=3_000):
                    raw = locator.inner_text().strip()
                    price = self._clean_price(raw)
                    if price:
                        logger.info("Price extracted [%s]: %s", selector, price)
                        return price
            except Exception:
                continue

        logger.warning("Price not found — returning 'N/A'")
        return "N/A"

    def get_title(self) -> str:
        """Return the product title."""
        try:
            return self.page.locator(self.PRODUCT_TITLE).inner_text().strip()
        except Exception:
            return "Unknown Product"

    def add_to_cart(self) -> bool:
        """
        Click 'Add to Cart' and wait for the confirmation banner.
        Returns True if confirmation is detected, False otherwise.
        """
        logger.info("Clicking 'Add to Cart'…")
        try:
            self.page.locator(self.ADD_TO_CART_BTN).wait_for(
                state="visible", timeout=15_000
            )
            self.page.locator(self.ADD_TO_CART_BTN).click()

            # Some pages redirect to cart, others show an inline confirmation
            try:
                self.page.wait_for_selector(self.CART_CONFIRM, timeout=10_000)
                logger.info("Cart confirmation banner detected.")
                return True
            except Exception:
                # Fallback: check if we landed on the cart page
                if "cart" in self.page.url:
                    logger.info("Redirected to cart page — item added.")
                    return True
                logger.warning("No cart confirmation detected.")
                return False
        except Exception as exc:
            logger.error("add_to_cart failed: %s", exc)
            return False

    # ── Private helpers ───────────────────────────────────────────
    @staticmethod
    def _clean_price(raw: str) -> str:
        """Strip whitespace / newlines and ensure a leading $."""
        # Remove line breaks Amazon sometimes injects
        cleaned = re.sub(r"\s+", "", raw)
        if cleaned and not cleaned.startswith("$"):
            cleaned = "$" + cleaned
        return cleaned
