# Results Summary

This document summarizes the performance of all evaluated trading strategies across
different assets and timeframes. The results are reported based on historical backtesting
using consistent evaluation metrics.

---

## Summary Table

| Strategy        | Time Period | Market | Profit (%) | Sharpe Ratio | Max Drawdown (%) | Annualized Returns (Final Balance) |
|-----------------|-------------|--------|------------|---------------|------------------|------------------------------------|
| EMA + ADX       | 1 day       | BTC    | 454.85     | 5.39          | 37.00            | 5548.59                            |
| EMA + ADX       | 1 day       | ETH    | 1154.54    | 7.06          | 42.00            | 12545.46                           |
| PVT + ADX       | 4 hr        | BTC    | 112.08     | -1.99         | 17.39            | 2120.81                            |
| PVT + ADX       | 4 hr        | ETH    | 2200.32    | 3.95          | 15.94            | 23003.25                           |
| PVT + ADX       | 1 day       | BTC    | 350.28     | 7.80          | 24.40            | 4502.87                            |
| PVT + ADX       | 1 day       | ETH    | 783.89     | 6.62          | 11.16            | 8838.92                            |
| EMA + ADX       | 4 hr        | BTC    | 489.07     | 3.32          | 37.80            | 5090.78                            |
| EMA + ADX       | 4 hr        | ETH    | 438.38     | 3.13          | 45.15            | 5384.85                            |
| Heikin Ashi | 30 mins | BTC    | 66.00      | 1.40          | 51.42            | 1664.38                            |

---

## Key Observations

- **EMA + ADX (1D)** performs consistently well on both BTC and ETH, achieving strong
  Sharpe ratios and high profitability.
- **PVT + ADX (1D)** shows particularly strong risk-adjusted performance on ETH,
  with the lowest drawdown among all strategies.
- **Intraday strategies (4H, 30M)** exhibit higher volatility and drawdowns,
  especially the Heikin Ashi + Kalman approach.
- ETH generally outperforms BTC in terms of absolute returns across most strategies.

---

## Plots and Visualizations

All output plots generated during individual experiments  
(cumulative returns, drawdowns, strategy returns) are stored in:

'''
results/plots/
'''


These plots are produced directly by the corresponding experiment notebooks and are
not regenerated in this summary file.

---

## Notes

- Backtests were conducted independently within each experiment notebook.
- Metrics were consolidated manually for clarity and reproducibility.
- CSV result files are intentionally excluded from version control.

---

