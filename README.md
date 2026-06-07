# Amazon Automation Suite 🛒

A professional end-to-end browser automation suite built with **Playwright + Python** using the **Page Object Model (POM)** design pattern. The suite automates product search and cart addition flows on Amazon, with full support for **parallel execution** and optional **LambdaTest cloud integration**.

---

## 📋 Test Scenarios

| ID   | Description                                  | Assertion                          |
|------|----------------------------------------------|------------------------------------|
| TC-1 | Search iPhone → Add to cart → Print price    | Cart confirmation + price printed  |
| TC-2 | Search Galaxy → Add to cart → Print price    | Cart confirmation + price printed  |

Both test cases run **in parallel** by default (`pytest-xdist -n 2`).

---

## 🏗️ Project Structure

```
amazon-automation/
│
├── config/
│   └── settings.py          # All configuration (URLs, timeouts, LT creds)
│
├── pages/                   # Page Object Model layer
│   ├── base_page.py         # Shared browser interaction helpers
│   ├── home_page.py         # Amazon landing page + search bar
│   ├── search_results_page.py  # Result grid interactions
│   └── product_page.py      # PDP: price extraction + add-to-cart
│
├── tests/
│   └── test_amazon_cart.py  # TC-1 and TC-2 test cases
│
├── utils/
│   └── logger.py            # Centralised logging factory
│
├── reports/                 # Auto-generated HTML reports + screenshots
├── conftest.py              # Pytest fixtures (browser, context, page)
├── pytest.ini               # Pytest settings
├── requirements.txt         # Python dependencies
└── .env.example             # Environment variable template
```

---

## ⚙️ Prerequisites

- Python **3.9+**
- pip
- Git

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/amazon-automation.git
cd amazon-automation
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install chromium
```

### 5. (Optional) Configure environment variables

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

---

## ▶️ Running the Tests

### Run both test cases **in parallel** (recommended)

```bash
pytest -n 2 tests/test_amazon_cart.py
```

### Run sequentially (for debugging)

```bash
pytest tests/test_amazon_cart.py
```

### Run a single test case

```bash
# TC-1 only
pytest tests/test_amazon_cart.py::test_iphone_search_and_add_to_cart

# TC-2 only
pytest tests/test_amazon_cart.py::test_galaxy_search_and_add_to_cart
```

### Run with visible browser (headed mode)

```bash
HEADLESS=false pytest -n 2 tests/test_amazon_cart.py
```

### Run on a specific browser

```bash
BROWSER=firefox pytest -n 2 tests/test_amazon_cart.py
```

---

## 📊 Reports

After each run an HTML report is generated automatically:

```
reports/report.html
```

Open it in any browser for a full summary with test statuses, durations, and logs.

Screenshots are captured at key steps (home, results, product, post-cart) and saved to `reports/`.

---

## ☁️ LambdaTest Cloud Integration (Bonus)

### 1. Sign up

Create a free account at [lambdatest.com](https://www.lambdatest.com) and grab your **Username** and **Access Key** from the dashboard.

### 2. Set credentials

Add them to your `.env` file:

```env
LT_USERNAME=your_lt_username
LT_ACCESS_KEY=your_lt_access_key
```

### 3. Run on the cloud

```bash
pytest -n 2 tests/test_amazon_cart.py
```

The suite auto-detects the LambdaTest credentials and routes execution through the **LambdaTest Playwright Grid** — no other code change needed.

You can monitor live test execution in the [LambdaTest Automation Dashboard](https://automation.lambdatest.com/).

---

## 🔑 Key Technical Highlights

| Feature                    | Implementation                                         |
|----------------------------|--------------------------------------------------------|
| Design Pattern             | Page Object Model (POM)                                |
| Parallel Execution         | `pytest-xdist` with `-n 2` workers                    |
| Multi-selector price logic | 6 fallback selectors to handle Amazon's dynamic DOM   |
| Cloud Integration          | LambdaTest via CDP endpoint, zero code change needed  |
| Screenshots                | Captured at every major step, saved to `reports/`     |
| HTML Reports               | `pytest-html` with self-contained single-file output  |
| Logging                    | Structured `logging` module with timestamps            |
| Configuration              | Environment-variable driven via `python-dotenv`        |

---

## 🧩 Design Decisions

**Why Playwright?**  
Playwright offers first-class async/parallel support, reliable auto-waiting, and a clean Python API. Its built-in CDP protocol also makes LambdaTest integration seamless.

**Why Page Object Model?**  
POM separates test logic from selector/interaction details, making the suite maintainable as Amazon's UI evolves. Adding a new page requires creating one class, not touching every test.

**Why multiple price selectors?**  
Amazon renders prices differently across product types (standard, deal, Kindle, third-party). The waterfall selector strategy ensures the suite is resilient to DOM variations without flakiness.

---

## 🐛 Troubleshooting

| Issue                          | Fix                                                         |
|--------------------------------|-------------------------------------------------------------|
| `TimeoutError` on search box   | Amazon may be rate-limiting. Try `SLOW_MO=500` in `.env`   |
| Price shows `N/A`              | Product may require sign-in. Try a different search query   |
| LambdaTest connection refused  | Verify `LT_USERNAME` and `LT_ACCESS_KEY` in `.env`         |
| `playwright install` fails     | Ensure you have the correct Python/pip version (3.9+)       |

---

## 📄 License

MIT © 2026
