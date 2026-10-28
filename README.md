# Hyperliquid Fundamental Analysis

A reproducible research snapshot of Hyperliquid's trading economics, stablecoin reserve income, competitive position and HYPE supply sensitivity.

**Research date: 28 October 2026. Economic observations through 27 October.**

**Research view: constructive on the operating platform; cautious on token valuation.** Buybacks connect protocol activity to HYPE demand, but revenue composition, future supply and valuation matter as much as headline volume.

Read the full [Russian research report](reports/hyperliquid_analysis_ru.md).

## Snapshot

| Metric | Value |
|---|---:|
| 30d fees, selected DefiLlama adapters | $80.04m |
| 30d protocol revenue, same scope | $63.87m |
| Trailing 365d protocol revenue | $686.23m |
| Annualized 30d protocol revenue | $777.09m |
| HYPE snapshot price | $80.52 |
| Circulating market cap | $19.28bn |
| Provider FDV | $76.62bn |
| Market cap / annualized revenue | 24.8x |
| FDV / annualized revenue | 98.6x |
| Circulating / current total supply | 25.16% |

Source: saved DefiLlama and CoinGecko connector responses. Annualized revenue is a run rate, not a forecast, earnings figure or measured buyback amount.

## What the research finds

- The selected DefiLlama perps adapter includes AQAv2 reserve income. It cannot be interpreted as pure trading fees.
- Token Terminal's separate product classification puts approximately 74% of retained 30d revenue in perps and 23% in USDC reserve income.
- Recent 30d economics softened against the previous 30 days in both providers, although scope and rates differ.
- Hyperliquid leads a five-venue Token Terminal comparison by notional volume. Its roughly 64% share is a selected-cohort share, not total-market share.
- Circulating valuation and diluted valuation tell materially different stories. Uncirculated supply is not an immediate sell forecast.
- Accrued reserve revenue, realized payments to the Assistance Fund and actual HYPE purchases are different observations. Actual purchases and net issuance remain unverified.

## Charts

![Monthly economics](charts/monthly_economics.png)

![Volume comparison](charts/peer_volume.png)

![Revenue sensitivity](charts/valuation_sensitivity.png)

The first and last months in the economics chart are partial. Scenario assumptions are illustrative; the valuation chart uses current total supply.

## Reproduce the saved snapshot

Python 3.11+:

```sh
python3 -m pip install -r requirements.txt
python3 run_analysis.py --offline
python3 -m unittest discover -s tests -v
```

The analysis performs no network requests. Package installation may require a network connection.

## Files

- `reports/hyperliquid_analysis_ru.md`: complete Russian report, source links and limitations.
- `data/raw/`: original connector responses plus an explicitly rounded transcription for comparison charts.
- `data/processed/summary.json`: derived metrics and calculation scope.
- `data/processed/economics.csv`: 7d, 30d, 90d and 365d metrics by adapter.
- `data/processed/peers.csv`: selected-cohort comparison.
- `data/processed/valuation_scenarios.csv`: revenue and supply sensitivity.
- `SOURCES.md`: source register, timestamp policy and unresolved reconciliation issues.
- `run_analysis.py`: offline calculations and chart generation.
- `tests/`: missing-data, date-window and valuation checks.

## Boundaries

DefiLlama and Token Terminal use different product scopes. Do not add provider totals or add ecosystem TVL to bridge and vault balances. Bridge-series coverage versus native USDC is unresolved. Daily charts exclude unfinished 28 October observations, including a duplicate date in the original bridge response.

Protocol revenue is not audited net income. HYPE is not equity and does not grant a contractual claim on revenue. No precise buyback yield, current HLP APY, full exploit history or verified contributor sale forecast is asserted.

This is a frozen research release; live updates are not implemented.

## Rights

Original Python code is provided under the MIT license in [LICENSE](LICENSE). Third-party data, documentation and research text are excluded from that code license; underlying providers retain their rights. No broader redistribution rights are asserted.
