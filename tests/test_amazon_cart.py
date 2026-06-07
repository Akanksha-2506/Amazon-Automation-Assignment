"""
tests/test_amazon_cart.py
--------------------------
Test Case 1 – iPhone search, add-to-cart, price verification
Test Case 2 – Galaxy device search, add-to-cart, price verification

Run in parallel:
    pytest -n 2 tests/test_amazon_cart.py
"""

import logging
import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from config.settings import IPHONE_QUERY, GALAXY_QUERY

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _run_search_and_add_to_cart(page, base_url: str, query: str, label: str) -> str:
    """
    Shared workflow:
      1. Open Amazon
      2. Search for `query`
      3. Open first result
      4. Extract & print price
      5. Add to cart
      6. Assert cart action succeeded
    Returns the extracted price string.
    """
    # ── Step 1: Open Amazon ───────────────────────────────────────
    home = HomePage(page)
    home.open(base_url)
    home.screenshot(f"{label}_01_home")

    # ── Step 2: Search ────────────────────────────────────────────
    home.search(query)
    home.screenshot(f"{label}_02_results")

    # ── Step 3: Click first result ────────────────────────────────
    results_page = SearchResultsPage(page)
    product_title = results_page.open_first_result()
    logger.info("[%s] Selected product: %s", label, product_title)

    # ── Step 4: Extract price ─────────────────────────────────────
    product_page = ProductPage(page)
    page.wait_for_load_state("domcontentloaded")
    price = product_page.get_price()
    full_title = product_page.get_title()

    # ── Print to console (as required by the assignment) ──────────
    print(f"\n{'='*60}")
    print(f"  [{label.upper()}] Product  : {full_title}")
    print(f"  [{label.upper()}] Price    : {price}")
    print(f"{'='*60}\n")

    home.screenshot(f"{label}_03_product")

    # ── Step 5: Add to cart ───────────────────────────────────────
    added = product_page.add_to_cart()
    home.screenshot(f"{label}_04_cart")

    # ── Step 6: Verify ────────────────────────────────────────────
    assert added, (
        f"[{label}] 'Add to Cart' did not succeed for: {full_title}"
    )
    logger.info("[%s] Successfully added to cart. Price: %s", label, price)
    return price


# ─────────────────────────────────────────────────────────────────────────────
# Test Cases
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.smoke
def test_iphone_search_and_add_to_cart(page, base_url):
    """
    TC-1: Search Amazon for an iPhone, add it to the cart, and
    print the device price to the console.
    """
    price = _run_search_and_add_to_cart(
        page=page,
        base_url=base_url,
        query=IPHONE_QUERY,
        label="iphone",
    )
    assert price != "N/A", "iPhone price was not extracted from the product page."


@pytest.mark.smoke
def test_galaxy_search_and_add_to_cart(page, base_url):
    """
    TC-2: Search Amazon for a Samsung Galaxy device, add it to the cart,
    and print the device price to the console.
    """
    price = _run_search_and_add_to_cart(
        page=page,
        base_url=base_url,
        query=GALAXY_QUERY,
        label="galaxy",
    )
    assert price != "N/A", "Galaxy price was not extracted from the product page."
