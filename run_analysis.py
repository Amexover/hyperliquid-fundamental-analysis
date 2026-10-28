"""Rebuild the frozen research snapshot without network access."""
import argparse
import csv
import json
import math
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data/raw"
OUT = ROOT / "data/processed"


def read(name):
    return json.loads((RAW / (name + ".json")).read_text(encoding="utf-8"))


def ratio(numerator, denominator):
    if numerator is None or denominator is None:
        return None
    if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator <= 0:
        return None
    return numerator / denominator


def daily_series(points, field="value_usd"):
    values = {}
    for point in points:
        day = date.fromisoformat(point["date"])
        value = point[field]
        if day in values:
            raise ValueError(f"Duplicate date: {day}")
        if value is None or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"Missing or non-finite value on {day}")
        values[day] = value
    if not values:
        raise ValueError("Empty daily series")
    return values


def window_sum(series, end, days):
    wanted = [end - timedelta(days=i) for i in range(days)]
    missing = [d for d in wanted if d not in series]
    if missing:
        raise ValueError(f"Incomplete {days}-day window: {missing[0]}")
    return sum(series[d] for d in wanted)


def export_csv(path, rows):
    if not rows:
        raise ValueError("Cannot export an empty table")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def calculate():
    products = {k: read(k)["data"] for k in ["perps", "spot"]}
    token = read("token")["data"]
    series = {
        (product, metric): daily_series(data[metric]["history"])
        for product, data in products.items()
        for metric in ["fees", "revenue"]
    }
    # Every product and measure must use the same completed-day cutoff.
    cutoff = min(max(values) for values in series.values())
    rows = []
    for (product, metric), values in series.items():
        row = {"product": product, "metric": metric, "cutoff": cutoff.isoformat()}
        for days in [7, 30, 90, 365]:
            row[f"usd_{days}d"] = window_sum(values, cutoff, days)
        previous = window_sum(values, cutoff - timedelta(days=30), 30)
        row["change_30d_pct"] = (ratio(row["usd_30d"], previous) - 1) * 100 if previous > 0 else None
        rows.append(row)

    def total(metric, days):
        return sum(row[f"usd_{days}d"] for row in rows if row["metric"] == metric)

    fees30, rev30 = total("fees", 30), total("revenue", 30)
    run_rate = rev30 * 365 / 30
    bridge_points = read("bridge")["data"]["points"]
    # The connector appends an intraday point with the same date as today's
    # daily point. Preserve both in raw data and exclude the unfinished day.
    bridge = daily_series([p for p in bridge_points if date.fromisoformat(p["date"]) <= cutoff], "tvl_usd")
    last = max(bridge)
    context = read("market_context")
    peers = context["peers"]
    denominator = sum(p["volume_30d_usd"] for p in peers)
    peer_rows = [{**p, "cohort_volume_share_pct": 100 * p["volume_30d_usd"] / denominator} for p in peers]
    summary = {
        "research_date": "2026-10-28",
        "economic_window_start": (cutoff - timedelta(days=29)).isoformat(),
        "economic_cutoff": cutoff.isoformat(),
        "scope": "DefiLlama perps adapter (includes AQAv2 reserve yield) + separate spot adapter; excludes separately measured HyperEVM and Outcomes",
        "fees_30d_usd": fees30,
        "revenue_30d_usd": rev30,
        "revenue_365d_usd": total("revenue", 365),
        "retained_share_pct": 100 * ratio(rev30, fees30),
        "revenue_run_rate_usd": run_rate,
        "market_cap_to_run_rate": ratio(token["market_cap"], run_rate),
        "fdv_to_run_rate": ratio(token["fully_diluted_valuation"], run_rate),
        "market_cap_to_trailing_revenue": ratio(token["market_cap"], total("revenue", 365)),
        "revenue_run_rate_to_market_cap_pct": 100 * ratio(run_rate, token["market_cap"]),
        "circulating_to_total_supply_pct": 100 * ratio(token["circulating_supply"], token["total_supply"]),
        "circulating_to_max_supply_pct": 100 * ratio(token["circulating_supply"], token["max_supply"]),
        "bridge_series_date": last.isoformat(),
        "bridge_intraday_latest_usd": bridge_points[-1]["tvl_usd"],
        "bridge_intraday_date": bridge_points[-1]["date"],
        "bridge_series_usd": bridge[last],
        "bridge_series_change_7d_pct": (ratio(bridge[last], bridge[last - timedelta(days=7)]) - 1) * 100,
        "bridge_series_change_30d_pct": (ratio(bridge[last], bridge[last - timedelta(days=30)]) - 1) * 100,
        "actual_buybacks_30d_usd": None,
        "net_income_usd": None,
    }
    scenarios = []
    # Sensitivity assumptions, deliberately not price forecasts.
    for growth, label in [(0.5, "Stress"), (1.0, "Flat"), (1.5, "Growth")]:
        for multiple in [15, 25, 35]:
            cap = run_rate * growth * multiple
            scenarios.append({
                "scenario": label, "revenue_factor": growth,
                "annual_revenue_usd": run_rate * growth,
                "revenue_multiple": multiple, "implied_capitalization_usd": cap,
                "price_current_circulating_usd": cap / token["circulating_supply"],
                "price_current_total_supply_usd": cap / token["total_supply"],
                "price_initial_max_supply_usd": cap / token["max_supply"],
            })
    return summary, rows, peer_rows, scenarios, series, bridge


def charts(series, bridge, peers, scenarios):
    from collections import defaultdict
    from chart_style import research_chart, save_chart, BLUE, MINT, MUTED, GRID
    import matplotlib.dates as mdates
    destination = ROOT / "charts"

    monthly = defaultdict(lambda: [0, 0])
    for (product, metric), values in series.items():
        for day, value in values.items():
            monthly[day.strftime("%Y-%m")][0 if metric == "fees" else 1] += value / 1e6
    keys = sorted(monthly)
    fig, ax = research_chart(
        "hyperliquid monthly fees & protocol revenue",
        "selected perps + spot adapters  |  usd millions",
    )
    x = list(range(len(keys)))
    ax.bar([i - .19 for i in x], [monthly[k][0] for k in keys], .38, label="Fees", color=BLUE)
    ax.bar([i + .19 for i in x], [monthly[k][1] for k in keys], .38, label="Protocol revenue", color=MINT)
    ax.set_xticks(x, [k + ("*" if k in [keys[0], keys[-1]] else "") for k in keys], rotation=45, ha="right")
    ax.set_ylabel("$M")
    ax.set_ylim(0, max(v[0] for v in monthly.values()) * 1.18)
    ax.legend(frameon=False, loc="upper left", ncol=2)
    save_chart(fig, ax, destination / "monthly_economics.png",
               "source: DefiLlama daily snapshots  |  through 27 Oct 2026",
               "* partial month  |  includes AQAv2 reserve income from Aug 2026")

    fig, ax = research_chart(
        "hyperliquid bridge series",
        "provider-reported balance  |  usd billions",
    )
    dates = sorted(bridge)
    balances = [bridge[d] / 1e9 for d in dates]
    ax.plot(dates, balances, color=BLUE, linewidth=2)
    ax.scatter([dates[-1]], [balances[-1]], color=MINT, s=25, zorder=4)
    ax.annotate(f"$"+"{:.2f}B".format(balances[-1]), (dates[-1], balances[-1]),
                xytext=(-8, 12), textcoords="offset points", ha="right",
                color=MINT, fontsize=10)
    ax.set_ylabel("$B")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    save_chart(fig, ax, destination / "bridge_series.png",
               "source: DefiLlama Hyperliquid Bridge  |  through 27 Oct 2026",
               "coverage versus native USDC is unresolved; not a measure of all client deposits")

    fig, ax = research_chart(
        "hyperliquid & perpetual exchange peers",
        "30-day notional volume  |  selected five-venue cohort  |  usd billions",
        left=0.18,
    )
    names = [p["name"] for p in peers][::-1]
    volumes = [p["volume_30d_usd"] / 1e9 for p in peers][::-1]
    ax.grid(False)
    ax.grid(axis="x", color=GRID, linewidth=.7)
    ax.barh(names, volumes, color=[MINT if n == "Hyperliquid" else BLUE for n in names], height=.56)
    ax.set_xlim(0, max(volumes) * 1.19)
    ax.set_xlabel("30-day volume ($B)", labelpad=10)
    for name, value in zip(names, volumes):
        ax.text(value + 3, name, f"$"+"{:.1f}B".format(value), va="center",
                color=MINT if name == "Hyperliquid" else MUTED, fontsize=10)
    save_chart(fig, ax, destination / "peer_volume.png",
               "source: Token Terminal connector, rounded values  |  28 Sep-27 Oct 2026",
               "cohort share is not total-market share; Aster volume is reported off-chain")

    fig, ax = research_chart(
        "hype valuation sensitivity",
        "annual revenue assumptions  |  current total supply of 951.54m hype",
    )
    for factor, label in [(0.5, "Stress: 0.5x"), (1.0, "Flat: 1.0x"), (1.5, "Growth: 1.5x")]:
        selected = [s for s in scenarios if s["revenue_factor"] == factor]
        ax.plot([s["revenue_multiple"] for s in selected],
                [s["price_current_total_supply_usd"] for s in selected],
                marker="o", markersize=5, linewidth=2, label=label)
    ax.set_xticks([15, 25, 35], ["15x", "25x", "35x"])
    ax.set_xlabel("Capitalization / annual protocol revenue", labelpad=10)
    ax.set_ylabel("Illustrative price ($/HYPE)")
    ax.set_ylim(0, max(s["price_current_total_supply_usd"] for s in scenarios) * 1.18)
    ax.legend(frameon=False, loc="upper left", ncol=3, fontsize=9)
    save_chart(fig, ax, destination / "valuation_sensitivity.png",
               "source: DefiLlama revenue + CoinGecko supply  |  research snapshot 28 Oct 2026",
               "illustrative assumptions, not price targets  |  annual revenue = 30d revenue x 365/30")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Rebuild from included snapshots (the only supported mode)")
    parser.parse_args()
    summary, rows, peers, scenarios, series, bridge = calculate()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    export_csv(OUT / "economics.csv", rows)
    export_csv(OUT / "peers.csv", peers)
    export_csv(OUT / "valuation_scenarios.csv", scenarios)
    charts(series, bridge, peers, scenarios)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
