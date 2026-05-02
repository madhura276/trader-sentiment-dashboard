# Bitcoin Market Sentiment vs Trader Performance Analysis

## Objective

The objective of this analysis is to explore the relationship between Bitcoin market sentiment and trader performance using the Fear/Greed index and historical trader data from Hyperliquid.

## Dataset Overview

The analysis uses two datasets:

1. Bitcoin Market Sentiment Dataset
2. Historical Trader Data from Hyperliquid

The datasets were merged using the trade date and sentiment date.

## Key Metrics by Sentiment

| classification   |   total_trades |   total_closed_pnl |   average_closed_pnl |   median_closed_pnl |   win_rate |   size_tokens_mean |
|:-----------------|---------------:|-------------------:|---------------------:|--------------------:|-----------:|-------------------:|
| Extreme Fear     |           2326 |     4399.94        |               1.8916 |              0      |    29.2777 |            2460.04 |
| Extreme Greed    |           5621 |        1.15689e+06 |             205.816  |              0.9605 |    55.3282 |           16407.3  |
| Fear             |          13869 |        1.77923e+06 |             128.288  |              0      |    38.1787 |            3219.87 |
| Greed            |          11292 |   609633           |              53.988  |              0      |    43.5707 |           14956.3  |
| Neutral          |           2756 |    74656.7         |              27.0888 |              0      |    49.492  |           17720.9  |

## Key Findings

- The sentiment category with the highest total closed PnL is **Fear**.
- The sentiment category with the highest average closed PnL is **Extreme Greed**.
- The sentiment category with the highest win rate is **Extreme Greed**.
- Trade count, profitability, average trade size, and leverage vary across different market sentiment conditions.
- The results suggest that trader behavior and performance are influenced by broader market sentiment.

## Long vs Short Performance

```txt
classification side  count           sum       mean
  Extreme Fear  BUY   1168 -3.794627e+03  -3.248825
  Extreme Fear SELL   1158  8.194564e+03   7.076480
 Extreme Greed  BUY   1661  1.502716e+04   9.047055
 Extreme Greed SELL   3960  1.141867e+06 288.350131
          Fear  BUY   7307  1.537586e+06 210.426466
          Fear SELL   6562  2.416394e+05  36.824047
         Greed  BUY   5407  8.468078e+04  15.661324
         Greed SELL   5885  5.249518e+05  89.201657
       Neutral  BUY   1020  1.273396e+04  12.484274
       Neutral SELL   1736  6.192278e+04  35.669805
``` 

## Top Accounts by PnL

```txt
                                   account   closed_pnl
0xb1231a4a2dd02f2276fa3c5e2a2f3436e6bfed23 1.478495e+06
0x083384f897ee0f19899168e3b1bec365f52a9012 9.655887e+05
0xbee1707d6b44d4d52bfe19e41f8a828645437aab 2.056523e+05
0xbaaaf6571ab7d571043ff1e313a9609a10637864 2.013539e+05
0x72c6a4624e1dffa724e6d00d64ceae698af892a0 1.972949e+05
0x75f7eeb85dc639d5e99c78f95393aa9a5f1170d4 1.425837e+05
0x513b8629fe877bb581bf244e326a047b249c4ff1 6.054430e+04
0x28736f43f1e871e6aa8b1148d38d4994275d72c4 5.853488e+04
0xbd5fead7180a9c139fa51a103cb6a2ce86ddb5c3 4.509997e+04
0x2c229d22b100a7beb69122eed721cee9b24011dd 4.304078e+04
```

## Most Traded Symbols

```txt
Symbol column was not available in the dataset.
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
