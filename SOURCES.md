# Sources and methodology

Retrieved on 28 October 2026. The original JSON responses include provider URLs and UTC retrieval timestamps. No API keys or wallet credentials are required by the offline analysis.

| File | Source | Coverage |
|---|---|---|
| data/raw/perps.json | DeFi Analyst → DefiLlama fees and revenue summaries | Daily observations, 28 Oct 2025–27 Oct 2026 |
| data/raw/spot.json | DeFi Analyst → DefiLlama fees and revenue summaries | Same window, separate Spot Orderbook adapter |
| data/raw/bridge.json | DeFi Analyst → DefiLlama Hyperliquid Bridge | Daily provider series plus intraday observation |
| data/raw/token.json | DeFi Analyst → CoinGecko hyperliquid | Market data updated 28 Oct, 20:48:50 UTC |
| data/raw/tt.md | Token Terminal research connector | Narrative/table response with rounded values, 30d and 90d windows ending 27 Oct |
| data/raw/market_context.json | Explicit transcription of tt.md and web page observations | Rounded secondary input; not a raw daily data export |

The daily DefiLlama responses are the computational source of truth for the selected adapter model. The connector's reported 30d totals match the 30 daily observations in each fee/revenue series.

## Public source links

- [DefiLlama Perps](https://defillama.com/protocol/hyperliquid-perps): metrics and current adapter scope.
- [DefiLlama Spot](https://defillama.com/protocol/hyperliquid-spot-orderbook): separate trading product.
- [DefiLlama Bridge](https://defillama.com/protocol/hyperliquid-bridge): provider TVL series.
- [CoinGecko HYPE](https://www.coingecko.com/en/coins/hyperliquid): price, supply and indicative unlock calendar.
- [Token Terminal](https://tokenterminal.com): actual retrieved connector response is preserved in tt.md; no raw SQL or daily peer export was returned.
- [About Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs).
- [Fees](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees).
- [AQAv2](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/aligned-quote-assets).
- [Current USDC infrastructure](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/usdc).
- [Staking](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking).
- [HLP](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/protocol-vaults).
- [HIP-3](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals).
- [HyperEVM](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm).
- [Audits](https://hyperliquid.gitbook.io/hyperliquid-docs/audits).
- [Hyperliquid Strategies annual disclosure](https://www.sec.gov/Archives/edgar/data/2078856/000119312526412579/d168610dars.pdf): third-party public-company description of contributor allocation and vesting; not a direct vesting-contract audit.
- [Bitwise prospectus](https://s3.us-east-1.amazonaws.com/static.bitwiseinvestments.com/bhyp/BHYP-Bitwise-Hyperliquid-ETF-Prospectus.pdf): first-party issuer risk disclosure discussing historical JELLY intervention; not a complete incident register.

Official documentation was read live through browsing. Search snippets sometimes expose earlier page versions: the report follows the opened current pages for USDC, AQAv2 and fee mechanics. Web pages are mutable; their full text is not archived here. Links document provenance, not an immutable source backup.

## Date and missing-data rules

1. All trading-economic windows use 27 October as the common closed-day cutoff.
2. A 30-day window means 28 September–27 October inclusive. A trailing 365-day window means 28 October 2025–27 October 2026.
3. Changes compare the latest 30-day sum with the immediately preceding 30-day sum.
4. Annualization uses 365/30. Trailing totals and annualized short-window totals remain separate.
5. Empty, missing, non-finite and duplicate daily observations fail calculations. Missing denominators return null, not zero.
6. The Bridge response contains two different values for 28 October. Both are preserved. For daily calculations both unfinished-day points are excluded; the final received point is retained separately as an intraday snapshot.
7. TVL is a stock; volume, fees and revenue are flows. Open interest is not summed over a period.
8. Peer input precision is limited by the rounded connector response. Cohort shares are recomputed, so they differ slightly from rounded shares quoted by Token Terminal.

## Unresolved issues

- DefiLlama perps includes trading, builder fees and AQAv2 reserve income; Token Terminal separately classifies reserve income, spot, HyperEVM and outcome markets. The providers are not a like-for-like reconciliation.
- DefiLlama 30d perps volume of about $206.19bn differs from Token Terminal's $231bn. Trade-level alignment was not performed.
- Token Terminal's returned product table includes a period sum of daily open-interest values. That sum is economically inappropriate and is not used. Only the final $7.83bn snapshot is used.
- Token Terminal returns project revenue-generating addresses, not a separately queried perps-active-trader cohort.
- Bridge-labelled TVL cannot be assumed to equal legacy Arbitrum escrow or total client deposits after native USDC migration.
- Current total supply and the initial maximum differ. The supplied FDV is used as returned, rather than silently replaced with price × initial maximum.
- Actual 30d buyback expenditure, HYPE burned, future net issuance and full operating costs are unavailable.
- CoinGecko's 6 November / 9.92m HYPE unlock is an indication, not an independently verified vesting forecast.
- No investment probability is assigned to the illustrative valuation cases.
- Historical Aave project figures are not reused as current comparative valuations.

## Refresh policy

This version does not contain a live data downloader. To refresh, obtain new connector responses, preserve retrieval metadata, reconcile scope changes and update the report date and narrative before publishing. Merely rerunning the calculation reproduces the existing snapshot.
