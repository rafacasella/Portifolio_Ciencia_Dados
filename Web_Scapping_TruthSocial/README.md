# 📊 Geopolitical & Economic Intelligence Monitor - Truth Social

This project consists of an automated pipeline for real-time data extraction and monitoring targeting the official profiles of public figures on the **Truth Social** platform. The system monitors mentions of strategic keywords related to global markets, economy, and geopolitical tensions.

Developed as a core component of my Data Science portfolio, this project overcomes the traditional challenges of web scraping (such as Cloudflare mitigation blocks, dynamic JavaScript rendering, and fragile CSS classes) by leveraging advanced stealth automation and network traffic interception techniques.

---
## 🧠 Architectural Overview & Concurrency Model

Integrating an asynchronous browser automation framework like **Playwright Async** inside a graphical user interface (GUI) poses significant thread-concurrency challenges. If executed on a single thread, the endless polling loop would starve the GUI event processor, causing the window to freeze.

To achieve non-blocking performance, this software implements a robust **Multithreading & Asynchronous Event Loop** architecture:

```text
 ┌────────────────────────────────────────────────────────┐
 │                   MAIN THREAD (GUI)                    │
 │  - CustomTkinter Window Loop (.mainloop())             │
 │  - Responsive User Input UI & Rendered Log Displays    │
 └───────────────────────────┬────────────────────────────┘
                             │ (Spawns on Start Button Click)
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │                 BACKGROUND THREAD                      │
 │  - Independent OS Worker Thread (threading.Thread)     │
 │  - Isolated Asyncio Event Loop (asyncio.new_event_loop)│
 │  ┌──────────────────────────────────────────────────┐  │
 │  │             PLAYWRIGHT ASYNC WORKER              │  │
 │  │  - Headless Chromium Interception Pipeline       │  │
 │  │  - Network Hook: Intercepts JSON REST API Traffic│  │
 │  └──────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────┘
```

### Key Technical Engineering Highlights
* **Network Response Interception**: Rather than relying on fragile HTML DOM parsing (which breaks often during layout changes), the core script registers a network hook (`page.on("response")`) to capture the underlying raw JSON payloads directly from the platform's endpoints, providing 100% data integrity.
* **Anti-Fingerprinting**: Injects automated fingerprint concealment scripts (`AutomationControlled` bypasses, custom User-Agents, and ASCII forced string routing) to mimic authentic humancentric navigation, bypassing Cloudflare's browser telemetry.

---

## 🛠️ Feature Engineering & Keyword Matching

The engine transforms raw text streams into directional risk signals by cleaning input metadata using RegEx tag stripping ($HTML \to Plain\ Text$) and executing an optimized matching vector against high-priority market targets:

$$\text{Match} = \{ w \in \text{Keywords} \mid w_{\text{lowercase}} \in \text{Text}_{\text{lowercase}} \}$$

When a hit occurs, the background worker thread safely pushes the memory block down to the UI console using standard terminal serialization strings.

---

## 💻 Technical Stack & Environment

### Dependencies
* Python 3.10+
* Playwright (Chromium Headless Core)
* CustomTkinter
* Asyncio / Threading

### System Requirements & Standalone Compilation
The source code has been successfully compiled into a **standalone native `.exe` binary** using PyInstaller. This encapsulates all required application hooks inside a single executable frame:

```bash
# To compile the standalone executable locally:
pip install customtkinter playwright pyinstaller
playwright install chromium
pyinstaller --noconsole --onefile truth_monitor_desktop.py
```
The compiled artifact will look for existing Chromium browser signatures on the host system machine's standard AppData environment local cache paths.

---

## 🚀 Execution Instructions

### Running from Python Source:
```bash
# 1. Navigate to the project directory
cd Web_Scapping_TruthSocial

# 2. Run the application
python truth_monitor_desktop.py
```

### UI Controls
1. **Target Input**: Configure any username string (Default: `realDonaldTrump`).
2. **Alert Keywords**: Comma-separated tracking parameters (e.g., `conflict, oil, tariffs`).
3. **Polling Interval**: Adjustable delay buffer parameter (in seconds) to control extraction frequency.