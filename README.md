# Crypto Algorithmic Trading Research

This repository presents a **research-focused study of algorithmic trading strategies**
applied to **cryptocurrency markets (BTC & ETH)** across multiple timeframes.

The project is structured to clearly separate:
- Data handling
- Strategy logic
- Experimental evaluation
- Result reporting

This is **not** a trading bot. It is a **systematic backtesting and analysis framework**.

---

## Motivation

This project was inspired by the **Inter IIT Tech Meet 2023 – Zelta Automations Trading Problem Statement**.
While the original problem focused on competition-driven strategy design, this repository
reframes the work as a **clean, reproducible research study** for analyzing technical
trading strategies under different market regimes.

---

## Repository Structure

```
crypto-algo-trading-research/
│
├── data/
│ ├── raw/ # Raw OHLCV data (not versioned)
│ ├── raw_processed/ # Cleaned & resampled datasets
│ ├── fetch_historical.py # Data download utilities
│ ├── preprocess.py # Data cleaning & resampling
│ └── README.md # Data documentation
│
├── docs/
│ ├── 2024_HighPrep_ZeltaAutomations.pdf
│ └── methodology.md
│
├── experiments/
│ ├── baseline/
│ │ ├── bb_atr.ipynb
│ │ ├── bb_rsi.ipynb
│ │ ├── macd_rsi.ipynb
│ │ └── parabolic_sar.ipynb
│ │
│ └── advanced/
│ ├── ema_adx.ipynb
│ ├── heiken_ashi_trend.ipynb
│ └── pvt_adx.ipynb
│
├── strategies/
│ ├── baseline/
│ │ ├── init.py
│ │ └── bb_atr.py
│ │
│ └── advanced/
│ ├── init.py
│ ├── ema_adx.py
│ ├── heiken_ashi_trend.py
│ └── pvt_adx.py
│
├── results/
│ ├── csv_outputs/ # Backtest summaries (ignored by git)
│ ├── plots/ # Equity curves & drawdown plots
│ └── results_summary.md
│
├── requirements.txt
├── README.md
└── LICENSE
```


---

## Strategy Overview

### Baseline Strategies
Simple, interpretable strategies used as reference benchmarks.

- **BB + ATR** – Volatility-based mean reversion
- **BB + RSI** – Momentum-filtered Bollinger strategy
- **MACD + RSI** – Trend-following baseline
- **Parabolic SAR** – Trend reversal detection

### Advanced Strategies
Multi-indicator strategies focusing on trend strength and market structure.

- **EMA + ADX** – Directional trend strength filtering
- **PVT + ADX** – Volume-confirmed trend detection
- **Heikin Ashi Trend** – Smoothed price action analysis

---

## Experiments

Each notebook inside `experiments/`:
- Loads processed OHLCV data from `data/raw_processed/`
- Imports strategy logic from `strategies/`
- Computes:
  - Strategy returns
  - Cumulative returns
  - Drawdown
- Generates plots saved to `results/plots/`

Experiments are intentionally **self-contained and reproducible**.

---

## Results

### Summary
A consolidated comparison of all strategies is available in:

```
results/results_summary.md
```


This includes:
- Profit percentage
- Sharpe ratio
- Maximum drawdown
- Final portfolio balance
- Asset and timeframe comparison

### Plots
All output visualizations (equity curves, drawdowns) are stored in:

```
results/plots/
```

### CSV Outputs
Intermediate backtest statistics are saved to:
```
results/csv_outputs/
```



---

## Design Philosophy

- ❌ No live trading
- ❌ No execution engine
- ❌ No hyperparameter optimization
- ❌ No claims of profitability
- ✅ Research-first structure
- ✅ Clear separation of concerns
- ✅ Reproducible experiments

---

## Setup

```bash
pip install -r requirements.txt
```


## Contributors
- Mandeep N H
- Pranav Raghuram
