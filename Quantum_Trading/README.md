# 🤖 AI-Driven Quantitative Trading Pipeline & Analytics Dashboard 
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://quantumtradingg.streamlit.app/?embed=true&embed_options=disable_light_theme)

An end-to-end quantitative finance pipeline that extracts historical market data, engineers technical and statistical features, trains a Machine Learning classifier to predict next-day directional movements, simulates rigorous backtesting, and deploys an interactive analytics dashboard.

---

## 📈 System Architecture

The project is structured as a modular Production-Grade ETL (Extract, Transform, Load) and Machine Learning pipeline:

```text
       [ yfinance API ]
              │
              ▼
    1. extract_and_prep.py  ──► Generates 'features_mercado.csv' (Technical Indicators)
              │
              ▼
    2. train.py             ──► Multi-Tree Random Forest Training & Probability Calculation
              │
              ▼
    3. backtest.py          ──► Vectorized Backtesting & Risk-Adjusted Metrics (Sharpe, MDD)
              │
              ▼
    4. app_streamlit.py     ──► Interactive UI Embedded into Live Web Portfolio
```

---

## 🛠️ Feature Engineering & Alpha Generation

To provide the Machine Learning model with predictive power (Alpha), raw pricing structures are transformed into statistical and momentum features:

* **Daily Log Returns**: Captures asset volatility and relative price changes.
* **Simple Moving Averages (SMA_10 / SMA_30)**: Identifies underlying macroeconomic and microeconomic trends.
* **Relative Strength Index (RSI_14)**: Measures velocity and magnitude of directional price movements to detect overbought or oversold conditions.
* **Bollinger Bands (20, 2)**: Quantifies historical standard deviations and price dispersion thresholds.

### The Predictive Target
The mathematical target ($Y$) is modeled as a binary classification problem:
$$Y_t = \begin{cases} 1 & \text{if } \text{Close}_{t+1} > \text{Close}_t \\ 0 & \text{otherwise} \end{cases}$$
The model predicts the probability $P(Y_t = 1 \mid X_t)$ to generate direction signals.

---

## 📊 Quant Metrics & Risk Framework

This system implements rigorous evaluation protocols to prevent backtest overfitting (*overfitting bias*) and data leakage (*look-ahead bias*):

* **Strict Time-Series Split**: The data is partitioned chronologically (80% Training / 20% Out-of-Sample Testing). Random K-Fold cross-validation is strictly avoided to preserve temporal causality.
* **Vectorized Execution**: Trades are simulated by shifting machine learning signals by one full session ($\text{Signal}_{t-1}$), guaranteeing that execution parameters depend only on information available *prior* to market opening.

### Key Performance Indicators (KPIs)
* **Sharpe Ratio (Annualized)**: Measures risk-adjusted excess returns over volatility.
* **Maximum Drawdown (MDD)**: The peak-to-trough decline during a specific record period, indicating absolute capital risk exposure.
* **Benchmark Comparison**: All returns are evaluated against a pure passive benchmark strategy (*Buy & Hold*).

---

## 💻 Technical Stack & Installation

### Requirements
* Python 3.9+
* Pandas / Numpy
* yfinance
* Scikit-Learn
* Streamlit / Plotly

### Setup Environment
```bash
# Clone the repository
git clone https://github.com
cd AI_Quant_Trading

# Install required dependencies
pip install -r requirements.txt
```

---

## 🚀 Execution Guide

Run the pipeline execution steps in chronological order:

```bash
# Step 1: Extract data and calculate features
python extract_and_prep.py

# Step 2: Train the Random Forest model and output probabilities
python train.py

# Step 3: Run the vectorized backtest engine
python backtest.py

# Step 4: Launch the interactive visualization dashboard
streamlit run app_streamlit.py
```

---

## 🎯 Portfolio Integration

The visualization dashboard is designed to be fully responsive, matching dark-ambient enterprise themes, and seamlessly embeds via raw CSS overlay components inside digital portfolio web designs.
