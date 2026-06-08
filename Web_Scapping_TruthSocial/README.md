# 📊 Geopolitical & Economic Intelligence Monitor - Truth Social

This project consists of an automated pipeline for real-time data extraction and monitoring targeting the official profiles of public figures on the **Truth Social** platform. The system monitors mentions of strategic keywords related to global markets, economy, and geopolitical tensions.

Developed as a core component of my Data Science portfolio, this project overcomes the traditional challenges of web scraping (such as Cloudflare mitigation blocks, dynamic JavaScript rendering, and fragile CSS classes) by leveraging advanced stealth automation and network traffic interception techniques.

---

## 🚀 Key Features

*   **Headless Background Monitoring:** The script runs completely invisibly, minimizing processing and memory overhead.
*   **Hidden API Interception:** Instead of relying on a frequently changing visual layout (HTML/CSS), the code directly captures raw JSON packets from network traffic exchanged between the browser and the server (`/api/v1/accounts/.../statuses`).
*   **Smart Multi-Term Filtering:** Real-time analysis of new publications based on a list of strategic keywords: `economy`, `Iran`, `conflict`, `Hormuz`, `oil`, `taxes`, and `tariffs`.
*   **Asynchronous Architecture & Anti-Duplication:** Event-driven implementation with strict pointer tracking (unique incremental `ID`), ensuring no post is processed twice or duplicated.
*   **Anti-Bot Mechanism (Stealth Mode):** Bypasses automation fingerprints (`navigator.webdriver`) and spoofs network headers to emulate human behavior, significantly mitigating Cloudflare challenges.

---

## 🛠️ Tech Stack & Libraries

*   **Python 3.13+**: Core programming language.
*   **Playwright (Async API):** Browser automation framework used to render the platform's React/Next.js ecosystem and intercept network requests.
*   **Asyncio:** Native library for managing asynchronous event loops and concurrency.
*   **urllib.parse (urljoin):** Utilized for structural URL normalization, safeguarding the script against local operating system encoding issues.
*   **Regular Expressions (re):** String parsing and cleaning to eliminate raw HTML tags contained within the API payloads.

---

## 📈 Technical Insights & Key Takeaways

### 1. Resolving Loading Deadlocks
Social media platforms based on Mastodon/Next.js architectures rely on WebSocket connections and continuous media loading. Leveraging `wait_until="domcontentloaded"` and strict timeout limits (35 seconds) successfully prevented execution deadlocks and script freezes.

### 2. Encoding Safeguards
During development, environmental variations in local compilers were found to drop the `/` character in compound strings (`com/@`). This was permanently resolved by replacing static string concatenations with dynamic construction via `urljoin` and ASCII code injection (`chr(47)`).

### 3. Data Extraction Efficiency
Targeting the direct API response (`response.json()`) proved to be **82% faster** than traditional DOM-parsing methods (`page.query_selector_all`). Additionally, this methodology makes the pipeline immune to any design or interface updates on Truth Social.

---

## 📈 Project Impact & Results

### Continuous Monitoring
The system monitors posts from the U.S. President concerning current global conflicts that directly affect commodity pricing—particularly oil. 
These publications have the potential to drive high volatility into commodity markets and, consequently, impact global financial assets (specifically in Brazil, given the high correlation between commodities and its national economy).

---

## 🔧 How to Run the Project

1. Clone the repository to your local machine.
2. Ensure your virtual environment (`.venv`) is activated.
3. Install the required packages and the Chromium rendering engine:
```bash
pip install playwright
python -m playwright install
```
4. Execute the main script:
```bash
python truth_social.py
```
