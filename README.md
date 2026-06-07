
Amazon Automation Suite

A robust browser automation framework built using Playwright and Python, following the Page Object Model (POM) design pattern for scalability and maintainability.

The framework automates key Amazon shopping workflows, including product search, product selection, price extraction, and cart operations. It supports parallel execution for faster test runs

TEST SCENARIOS -

TC-1: Search for an iPhone → Open Product → Add to Cart → Capture Price
Validation:
- Product is successfully added to the cart
- Product price is retrieved and displayed in the test output

TC-2: Search for a Samsung Galaxy device → Open Product → Add to Cart → Capture Price
Validation:
- Product is successfully added to the cart
- Product price is retrieved and displayed in the test output

Both scenarios are designed to run simultaneously using Pytest-Xdist.


PREREQUISITES -

- Python 3.9 or later
- pip
- Git


SETUP INSTRUCTIONS -

Clone the Repository

git clone https://github.com/<your-username>/amazon-automation.git
cd amazon-automation

Create a Virtual Environment

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

Windows:
python -m venv .venv
.venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Install Playwright Browser Binaries

playwright install chromium

Configure Environment Variables (Optional)

cp .env.example .env


RUNNING THE TESTS -

Run Both Tests in Parallel

pytest -n 2 tests/test_amazon_cart.py

Run Sequentially

pytest tests/test_amazon_cart.py

Run Individual Tests

pytest tests/test_amazon_cart.py::test_iphone_search_and_add_to_cart

pytest tests/test_amazon_cart.py::test_galaxy_search_and_add_to_cart

Run with Visible Browser

HEADLESS=false pytest -n 2 tests/test_amazon_cart.py

Run on Firefox

BROWSER=firefox pytest -n 2 tests/test_amazon_cart.py


REPORTING -

After execution, an HTML report is generated:

reports/report.html

The report includes:
- Test execution summary
- Pass/fail status
- Execution duration
- Detailed logs

Screenshots are captured throughout the execution flow and stored in the reports directory.



KEY FEATURES -

- Page Object Model (POM) architecture
- Parallel execution using pytest-xdist
- Multiple fallback selectors for resilient price extraction
- Cross-browser support
- HTML reporting with pytest-html
- Automatic screenshot capture
- Structured logging with timestamps
- Environment-driven configuration
- Easy scalability for new test scenarios

