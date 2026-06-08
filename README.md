# 📊 Data Science Portfolio

Welcome to my project portfolio. Here, I showcase solutions developed to solve complex, real-world problems, covering the entire data lifecycle: from **real-time data extraction and engineering** to **predictive modeling using Deep Learning**.

My goal is to transform raw, unstructured data streams into automated strategic insights.

---

## 📂 Featured Projects

### 1. 📈 Stock Price Prediction using LSTM Neural Networks
**Domain:** *Deep Learning, Time Series Forecasting, Quantitative Finance*

This project develops a high-precision predictive model for financial time series, focusing on asset price volatility and closing trends in the stock market.

*   **The Problem:** Stock prices possess complex temporal dependencies and short-term noise, rendering traditional regression models inefficient.
*   **The Solution:** Implementation of a **Recurrent Neural Network (RNN)** using **LSTM (Long Short-Term Memory)** architecture, capable of retaining long-term patterns in time series without suffering from the vanishing gradient problem.
*   **Technical Approach:**
    *   **Preprocessing:** Historical data cleaning and scale normalization using Scikit-Learn's `MinMaxScaler`.
    *   **Modeling:** Architecture built with *TensorFlow/Keras*, stacking LSTM layers with regularization mechanisms (`Dropout`) to mitigate overfitting.
    *   **Validation:** Evaluation based on rigorous error metrics, such as RMSE (Root Mean Squared Error) and MAE (Mean Absolute Error).
*   **Core Technologies:** `TensorFlow`, `Keras`, `Scikit-Learn`, `Pandas`, `Matplotlib`.
*   **Where to Find:** `/Stock_Price_Prediction_LSTM` folder

---

### 📊 2. Geopolitical & Economic Intelligence Monitor (Truth Social)
**Domain:** *Data Engineering, Real-Time Streaming, Advanced Web Scraping*

An automated pipeline for real-time data extraction and monitoring targeting official profiles of public figures on the **Truth Social** platform. The system monitors mentions of strategic terms related to the market, oil, and geopolitical tensions.

*   **The Problem:** Modern platforms utilize SPA ecosystems (React/Next.js) and strict firewalls (Cloudflare), blocking traditional scrapers (like BeautifulSoup) or causing loading deadlocks.
*   **The Solution:** An asynchronous bot programmed in *Stealth* mode that, instead of parsing the visual HTML layout, **intercepts raw JSON API packets** within the browser network traffic.
*   **Technical Approach:**
    *   **Stealth Mode:** Script injection to mask automation variables (`navigator.webdriver`) and emulate human behavior.
    *   **Optimization:** Dynamic blocking of media assets (images/fonts) to speed up synchronization by 82% and save processing power.
    *   **String Robustness:** Structural handling of URLs via ASCII tables to safeguard the script against local compiler text encoding failures.
*   **Core Technologies:** `Playwright (Async API)`, `Asyncio`, `Regular Expressions (re)`, `Urllib`.
*   **Where to Find:** `/Web_Scapping_TruthSocial` folder

---

## 🛠️ Core Tech Stack

*   **Programming Languages:** Python (Pandas, NumPy, SciPy)
*   **Artificial Intelligence & Deep Learning:** TensorFlow, Keras, Scikit-Learn
*   **Data Engineering & Automation:** Playwright, Asyncio, Requests, RESTful APIs
*   **Environments & Tools:** PyCharm, Git, Virtual Environments (.venv)

---

## 📈 Key Outcomes & Skills Demonstrated

1.  **Time Series Expertise:** Ability to prepare the three-dimensional matrices required by Deep Learning models (`[samples, time steps, features]`) and fine-tune neural network hyperparameters for financial forecasting.
2.  **Resilient Data Engineering:** Development of scripts built to handle network failures, server fluctuations, and automated anti-bot blocks on web platforms.
3.  **Clean & Asynchronous Code:** Advanced application of event-driven and asynchronous programming (`async/await`) in Python for high-performance optimization.
