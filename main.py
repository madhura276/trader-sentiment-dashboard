import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
CHART_DIR = "charts"
REPORT_DIR = "reports"

TRADER_FILE = os.path.join(RAW_DIR, "historical_trader_data.csv")
SENTIMENT_FILE = os.path.join(RAW_DIR, "fear_greed_index.csv")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")


def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def find_column(df, keywords):
    for col in df.columns:
        if all(keyword in col for keyword in keywords):
            return col
    return None


def save_chart(path):
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    print("Loading datasets...")

    trader = pd.read_csv(TRADER_FILE)
    sentiment = pd.read_csv(SENTIMENT_FILE)

    trader = clean_columns(trader)
    sentiment = clean_columns(sentiment)

    print("Trader columns:", trader.columns.tolist())
    print("Sentiment columns:", sentiment.columns.tolist())

    sentiment_date_col = find_column(sentiment, ["date"]) or sentiment.columns[0]
    sentiment_class_col = find_column(sentiment, ["classification"]) or sentiment.columns[-1]

    sentiment[sentiment_date_col] = pd.to_datetime(sentiment[sentiment_date_col], errors="coerce")
    sentiment["date"] = sentiment[sentiment_date_col].dt.date
    sentiment["classification"] = sentiment[sentiment_class_col].astype(str).str.strip()

    time_col = find_column(trader, ["time"]) or find_column(trader, ["timestamp"])
    pnl_col = find_column(trader, ["closedpnl"]) or find_column(trader, ["closed", "pnl"])
    size_col = find_column(trader, ["size"])
    side_col = find_column(trader, ["side"])
    account_col = find_column(trader, ["account"])
    symbol_col = find_column(trader, ["symbol"])
    leverage_col = find_column(trader, ["leverage"])
    price_col = find_column(trader, ["execution", "price"]) or find_column(trader, ["price"])

    if time_col is None:
        raise ValueError("Could not find time column in trader dataset.")
    if pnl_col is None:
        raise ValueError("Could not find closedPnL column in trader dataset.")

    trader[time_col] = pd.to_datetime(trader[time_col], errors="coerce")
    trader["date"] = trader[time_col].dt.date

    numeric_cols = [pnl_col, size_col, leverage_col, price_col]
    for col in numeric_cols:
        if col and col in trader.columns:
            trader[col] = pd.to_numeric(trader[col], errors="coerce")

    merged = trader.merge(
        sentiment[["date", "classification"]],
        on="date",
        how="left"
    )

    merged = merged.dropna(subset=["classification", pnl_col])
    merged["is_win"] = merged[pnl_col] > 0

    merged.to_csv(os.path.join(PROCESSED_DIR, "merged_trader_sentiment.csv"), index=False)

    print("Merged rows:", len(merged))

    # Performance metrics by sentiment
    agg_dict = {
        pnl_col: ["count", "sum", "mean", "median"],
        "is_win": "mean"
    }

    if size_col:
        agg_dict[size_col] = "mean"
    if leverage_col:
        agg_dict[leverage_col] = "mean"

    sentiment_metrics = merged.groupby("classification").agg(agg_dict)
    sentiment_metrics.columns = [
        "_".join(col).strip("_") for col in sentiment_metrics.columns.values
    ]
    sentiment_metrics = sentiment_metrics.rename(columns={
        f"{pnl_col}_count": "total_trades",
        f"{pnl_col}_sum": "total_closed_pnl",
        f"{pnl_col}_mean": "average_closed_pnl",
        f"{pnl_col}_median": "median_closed_pnl",
        "is_win_mean": "win_rate"
    })
    sentiment_metrics["win_rate"] = sentiment_metrics["win_rate"] * 100
    sentiment_metrics.to_csv(os.path.join(PROCESSED_DIR, "sentiment_metrics.csv"))

    # Chart 1: Total PnL by sentiment
    plt.figure(figsize=(8, 5))
    plot_data = sentiment_metrics.reset_index().sort_values("total_closed_pnl", ascending=False)
    sns.barplot(data=plot_data, x="classification", y="total_closed_pnl", palette="viridis")
    plt.title("Total Closed PnL by Market Sentiment")
    plt.xlabel("Market Sentiment")
    plt.ylabel("Total Closed PnL")
    save_chart(os.path.join(CHART_DIR, "total_pnl_by_sentiment.png"))

    # Chart 2: Average PnL by sentiment
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_data, x="classification", y="average_closed_pnl", palette="mako")
    plt.title("Average Closed PnL by Market Sentiment")
    plt.xlabel("Market Sentiment")
    plt.ylabel("Average Closed PnL")
    save_chart(os.path.join(CHART_DIR, "avg_pnl_by_sentiment.png"))

    # Chart 3: Win rate by sentiment
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_data, x="classification", y="win_rate", palette="crest")
    plt.title("Win Rate by Market Sentiment")
    plt.xlabel("Market Sentiment")
    plt.ylabel("Win Rate (%)")
    save_chart(os.path.join(CHART_DIR, "win_rate_by_sentiment.png"))

    # Chart 4: Trade count by sentiment
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_data, x="classification", y="total_trades", palette="flare")
    plt.title("Trade Count by Market Sentiment")
    plt.xlabel("Market Sentiment")
    plt.ylabel("Number of Trades")
    save_chart(os.path.join(CHART_DIR, "trade_count_by_sentiment.png"))

    # Chart 5: PnL distribution
    plt.figure(figsize=(9, 5))
    sns.histplot(data=merged, x=pnl_col, hue="classification", kde=True, bins=50)
    plt.title("Closed PnL Distribution by Sentiment")
    plt.xlabel("Closed PnL")
    plt.ylabel("Frequency")
    save_chart(os.path.join(CHART_DIR, "pnl_distribution_by_sentiment.png"))

    # Chart 6: Leverage by sentiment
    if leverage_col:
        plt.figure(figsize=(9, 5))
        sns.boxplot(data=merged, x="classification", y=leverage_col)
        plt.title("Leverage Distribution by Market Sentiment")
        plt.xlabel("Market Sentiment")
        plt.ylabel("Leverage")
        save_chart(os.path.join(CHART_DIR, "leverage_by_sentiment.png"))

    # Chart 7: Size by sentiment
    if size_col:
        plt.figure(figsize=(9, 5))
        sns.boxplot(data=merged, x="classification", y=size_col)
        plt.title("Trade Size Distribution by Market Sentiment")
        plt.xlabel("Market Sentiment")
        plt.ylabel("Trade Size")
        save_chart(os.path.join(CHART_DIR, "trade_size_by_sentiment.png"))

    # Long vs short performance
    side_summary_text = "Side column was not available in the dataset."
    if side_col:
        side_perf = merged.groupby(["classification", side_col])[pnl_col].agg(["count", "sum", "mean"]).reset_index()
        side_perf.to_csv(os.path.join(PROCESSED_DIR, "side_performance.csv"), index=False)

        plt.figure(figsize=(10, 5))
        sns.barplot(data=side_perf, x="classification", y="sum", hue=side_col)
        plt.title("Long vs Short Total PnL by Sentiment")
        plt.xlabel("Market Sentiment")
        plt.ylabel("Total Closed PnL")
        save_chart(os.path.join(CHART_DIR, "side_pnl_by_sentiment.png"))

        side_summary_text = side_perf.to_string(index=False)

    # Top accounts by PnL
    account_summary_text = "Account column was not available in the dataset."
    if account_col:
        top_accounts = (
            merged.groupby(account_col)[pnl_col]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        top_accounts.to_csv(os.path.join(PROCESSED_DIR, "top_accounts.csv"), index=False)

        plt.figure(figsize=(10, 5))
        sns.barplot(data=top_accounts, x=pnl_col, y=account_col, palette="viridis")
        plt.title("Top 10 Accounts by Total Closed PnL")
        plt.xlabel("Total Closed PnL")
        plt.ylabel("Account")
        save_chart(os.path.join(CHART_DIR, "top_accounts_by_pnl.png"))

        account_summary_text = top_accounts.to_string(index=False)

    # Most traded symbols
    symbol_summary_text = "Symbol column was not available in the dataset."
    if symbol_col:
        top_symbols = merged[symbol_col].value_counts().head(10).reset_index()
        top_symbols.columns = ["symbol", "trade_count"]
        top_symbols.to_csv(os.path.join(PROCESSED_DIR, "top_symbols.csv"), index=False)

        plt.figure(figsize=(10, 5))
        sns.barplot(data=top_symbols, x="trade_count", y="symbol", palette="mako")
        plt.title("Top 10 Most Traded Symbols")
        plt.xlabel("Trade Count")
        plt.ylabel("Symbol")
        save_chart(os.path.join(CHART_DIR, "top_symbols.png"))

        symbol_summary_text = top_symbols.to_string(index=False)

    # Build report
    best_sentiment_total = sentiment_metrics["total_closed_pnl"].idxmax()
    best_sentiment_avg = sentiment_metrics["average_closed_pnl"].idxmax()
    best_win_sentiment = sentiment_metrics["win_rate"].idxmax()

    report = f"""# Bitcoin Market Sentiment vs Trader Performance Analysis

## Objective

The objective of this analysis is to explore the relationship between Bitcoin market sentiment and trader performance using the Fear/Greed index and historical trader data from Hyperliquid.

## Dataset Overview

The analysis uses two datasets:

1. Bitcoin Market Sentiment Dataset
2. Historical Trader Data from Hyperliquid

The datasets were merged using the trade date and sentiment date.

## Key Metrics by Sentiment

{sentiment_metrics.round(4).to_markdown()}

## Key Findings

- The sentiment category with the highest total closed PnL is **{best_sentiment_total}**.
- The sentiment category with the highest average closed PnL is **{best_sentiment_avg}**.
- The sentiment category with the highest win rate is **{best_win_sentiment}**.
- Trade count, profitability, average trade size, and leverage vary across different market sentiment conditions.
- The results suggest that trader behavior and performance are influenced by broader market sentiment.

## Long vs Short Performance

```txt
{side_summary_text}
``` 

## Top Accounts by PnL

```txt
{account_summary_text}
```

## Most Traded Symbols

```txt
{symbol_summary_text}
```
## Chart Interpretation

The total PnL and average PnL charts help compare profitability across sentiment categories.
The win rate chart highlights whether traders were more accurate during Fear, Greed, or other sentiment states.
The PnL distribution chart shows the spread of profits and losses under different sentiment conditions.
The leverage and trade size boxplots help identify whether traders took higher risk during certain sentiment periods.
The long vs short chart helps compare directional trading performance across sentiment groups.

## Strategy Insights

- If profitability is higher during Greed, traders may benefit from momentum-following strategies during optimistic market periods.
- If win rate is stronger during Fear, defensive or contrarian strategies may be useful.
- Higher leverage during specific sentiment periods should be treated carefully because it can increase both profit and loss.
- Top-performing accounts can be studied separately to understand whether consistent profitability comes from position sizing, timing, or market direction.
- Sentiment can be used as an additional feature in trading strategy design, but it should not be used alone.

## Conclusion

This analysis shows that market sentiment provides useful context for evaluating trader performance. By combining sentiment labels with trade-level performance metrics, it becomes possible to identify patterns in profitability, risk-taking, and trading behavior across different market conditions.
"""

    # save report
    with open(os.path.join(REPORT_DIR, "summary_report.md"), "w", encoding="utf-8") as f:
        f.write(report)

    print("Analysis completed.")
    print("Processed files saved in data/processed.")
    print("Charts saved in charts.")
    print("Report saved in reports/summary_report.md.")


if __name__ == "__main__":
    main()