# Hyperliquid Fundamental Analysis

Fundamental research on Hyperliquid and HYPE, covering trading economics,
stablecoin reserve income, competitive positioning and token valuation.

**Research view: constructive on the business, cautious on HYPE valuation.**

Hyperliquid generates substantial protocol revenue and links part of its
economics to HYPE purchases and burns. The investment question is whether that
demand can keep pace with the token's future supply and the growth already
reflected in its price.

[Full report in Russian](reports/hyperliquid_analysis_ru.md) ·
[Sources and methodology](SOURCES.md) · [MIT license](LICENSE)

> **Snapshot: 28 October 2026.** Daily economics end on 27 October.
> Market data and token supply are dated 28 October. This repository reproduces
> that research snapshot; it does not provide live market data.

## Investment snapshot

| Metric | Value |
|---|---:|
| 30d fees | $80.04m |
| 30d protocol revenue | $63.87m |
| Trailing 365d protocol revenue | $686.23m |
| Annualized 30d protocol revenue | $777.09m |
| HYPE price | $80.52 |
| Circulating market capitalization | $19.28bn |
| Fully diluted valuation reported by CoinGecko | $76.62bn |
| Market cap / annualized protocol revenue | 24.8x |
| FDV / annualized protocol revenue | 98.6x |
| Circulating / current total supply | 25.16% |

Economics use the saved DefiLlama Perps and Spot Orderbook adapters.
The Perps adapter also includes AQAv2 stablecoin reserve income.
Annualized revenue is a 30-day run rate, not a forecast or audited earnings.

## Key findings

- **Revenue is meaningful, but its composition matters.** Token Terminal's
  separate product breakdown attributes roughly 74% of retained 30d revenue to
  perps and 23% to USDC reserves. Reserve income should not be mistaken for
  growth in trading demand.
- **Recent economics softened.** In the DefiLlama Perps adapter, 30d fees fell
  10.1% and revenue fell 12.4% against the preceding 30 days.
- **Hyperliquid leads the selected peer group by volume.** Its roughly 64%
  share refers to the five venues compared here, not the entire perps market.
- **Supply changes the valuation picture.** Market cap / revenue run rate is
  24.8x, while the provider's FDV / revenue run rate is 98.6x.
- **Buybacks need a separate reconciliation.** Accrued revenue, payments to the
  Assistance Fund and executed purchases have different timing. Actual 30d
  buybacks and net issuance were not independently established.

## Protocol economics

![Monthly fees and protocol revenue](charts/monthly_economics.png)

The gap between fees and retained revenue reflects distributions and other
pass-through flows. The first and last months are partial and marked with an
asterisk. AQAv2 adds reserve income from August 2026, so the series is not a
constant-scope measure of trading revenue.

**Fees ≠ protocol revenue ≠ net income ≠ executed HYPE buybacks.**

## Competitive position

![Perpetual exchange volume comparison](charts/peer_volume.png)

The five-venue comparison uses Token Terminal data for the same 30-day window:
Hyperliquid, Lighter, Aster, GMX and dYdX. Values are rounded; Aster's volume is
reported off-chain. Nominal volume alone does not establish liquidity quality,
user retention or profitability.

Token Terminal reports approximately $231bn of Hyperliquid perps volume;
the viewed DefiLlama snapshot reports $206.19bn. These provider figures have
not been reconciled trade by trade. They are kept separate throughout the
research.

## Token valuation

![HYPE valuation sensitivity](charts/valuation_sensitivity.png)

The chart shows how revenue assumptions and valuation multiples affect an
illustrative price using **current total supply of 951.54m HYPE**. The CSV also
includes current circulating supply and the initial 1bn maximum.

| Scenario | Annual revenue | Revenue multiple | Price using current total supply |
|---|---:|---:|---:|
| Stress: 0.5x current run rate | ~$389m | 15x | ~$6 |
| Flat: 1.0x | ~$777m | 25x | ~$20 |
| Growth: 1.5x | ~$1,166m | 35x | ~$43 |

These are sensitivity cases, not price targets. The model does not forecast
the timing of emissions, future burns or operating costs.
[View the complete scenario grid](data/processed/valuation_scenarios.csv).

## Capital and data coverage

![Hyperliquid Bridge provider series](charts/bridge_series.png)

The chart preserves DefiLlama's **Hyperliquid Bridge** series. Its coverage
relative to native USDC remains unresolved: it should not be interpreted as
all client deposits or the balance of the legacy Arbitrum bridge.
The report explains this limitation and excludes unfinished-day observations.

## Methodology and limitations

| Input | Source | Use |
|---|---|---|
| Daily fees and revenue | DefiLlama via DeFi Analyst | Economic trends and main valuation model |
| Price and token supply | CoinGecko via DeFi Analyst | Circulating and diluted valuation |
| Product breakdown and peers | Token Terminal connector | Revenue composition and volume comparison |
| Mechanics and risks | Hyperliquid documentation and linked disclosures | Interpretation of the metrics |

Original connector responses are saved in [data/raw](data/raw).
Rounded peer inputs are identified explicitly. All calculations use completed
daily windows; missing observations are rejected rather than replaced with zero.

Protocol revenue is not audited net income, and HYPE does not grant a
contractual claim on revenue. Actual buybacks, net issuance, current HLP APY
and full operating expenses remain unverified. Provider TVL and product
totals are not added across overlapping scopes.

See [SOURCES.md](SOURCES.md) for dates, source links and unresolved differences.

## Reproduce the analysis

Python 3.11 or later:

```sh
python3 -m pip install -r requirements.txt
python3 run_analysis.py --offline
python3 -m unittest discover -s tests -v
```

The calculation and chart generation run locally from the included data.
Installing dependencies may require internet access. A rerun rebuilds the
saved snapshot; it does not fetch new prices or refresh the report.

## Repository guide

| Path | Contents |
|---|---|
| [reports](reports) | Full Russian report, risks and comparison with Aave |
| [data/raw](data/raw) | Source snapshots and rounded comparison inputs |
| [data/processed](data/processed) | Economic metrics, peer shares and valuation scenarios |
| [charts](charts) | Four charts in the shared Aave research style |
| [run_analysis.py](run_analysis.py) | Offline calculations and chart generation |
| [chart_style.py](chart_style.py) | Shared palette, typography and rounded chart rendering |
| [tests](tests) | Date-window, missing-data and valuation checks |

## License

The original Python code and its software documentation are available under
the [MIT License](LICENSE), copyright © 2026 Philipp Lebedev.

Research reports, datasets and generated research figures are outside that
software license. Third-party providers retain their rights.
See [DATA_LICENSE.md](DATA_LICENSE.md) for the scope and attribution policy.
