# 📊 Bitcoin Market Sentiment vs Trader Performance Dashboard

## 🚀 Live Demo

👉 https://trader-sentiment-dashboard-vfvqnctt2appevqbimfwav9.streamlit.app/

---

In addition to the required analysis, I built an interactive Streamlit dashboard to explore trader performance across market sentiment conditions in real-time.

The project includes:
- Data preprocessing and merging pipeline
- Sentiment-wise performance analysis
- Visual insights and distribution analysis
- Interactive dashboard for dynamic exploration

Live dashboard link: https://trader-sentiment-dashboard-vfvqnctt2appevqbimfwav9.streamlit.app/

GitHub repository: https://github.com/madhura276/trader-sentiment-dashboard

# 🧩 Problem Statement

Financial markets are heavily influenced by **investor sentiment** (Fear vs Greed), but:

* Traders often rely only on price-based indicators
* There is limited visibility into how **sentiment impacts actual trading performance**
* No clear data-driven understanding of:

  * When traders perform best
  * Whether fear or greed leads to better outcomes
  * How risk-taking behavior changes with sentiment

👉 The challenge:
**Can we quantify how market sentiment affects trader profitability and behavior?**

---

# 💡 Solution

This project builds a **data-driven analytics system** that:

1. Combines:

   * 📉 Bitcoin Fear/Greed Index (market sentiment)
   * 📊 Historical trader performance data

2. Processes and merges both datasets by date

3. Generates:

   * Performance metrics (PnL, win rate, trade count)
   * Behavioral insights (leverage, trade size, direction)

4. Visualizes everything in an:

   * ⚡ Interactive Streamlit dashboard
   * 📊 Real-time filtering + charts

👉 Result:
A complete system to **analyze trader performance under different market sentiments**

---

# ❗ Why This Matters

Understanding sentiment-driven behavior helps:

* 📈 Traders → Improve timing & strategy
* 🏦 Analysts → Study market psychology
* 🤖 Quant engineers → Build better models
* 📊 Data scientists → Add sentiment as a predictive feature

👉 Key idea:
**Markets are not just numbers — they reflect human emotion**

---

# ⚙️ What This Project Does

✔ Cleans and processes raw trading data
✔ Aligns it with sentiment data by date
✔ Calculates performance metrics per sentiment
✔ Generates charts and reports
✔ Builds an interactive dashboard for exploration

---

# 🔄 End-to-End Process

## 1. Data Collection

* Trader dataset (Hyperliquid trades)
* Sentiment dataset (Fear/Greed Index)

## 2. Data Cleaning

* Standardize column names
* Convert timestamps → date
* Handle missing values

## 3. Data Merging

* Merge on **date**
* Attach sentiment label to each trade

## 4. Feature Engineering

* Win/Loss classification
* Aggregated metrics:

  * Total PnL
  * Average PnL
  * Win rate
  * Trade count

## 5. Analysis

* Sentiment-wise performance comparison
* Long vs short analysis
* Top traders
* Most traded coins

## 6. Visualization

* Static charts (Matplotlib/Seaborn)
* Interactive charts (Plotly)

## 7. Dashboard

* Built using Streamlit
* Includes filters, metrics, charts

---

# 📊 Key Features

* 🔍 Sentiment-based filtering
* 📈 Performance metrics dashboard
* 📊 Interactive PnL charts
* 📉 Distribution analysis
* 📈 Cumulative PnL over time
* 🏆 Top trader analysis
* 💰 Most traded coins
* 🧠 Insight generation

---

# 📁 Project Structure (Explained)

```txt
primetrade-sentiment-trader-analysis/

├── data/
│   ├── raw/
│   │   ├── historical_trader_data.csv     # Raw trade-level dataset
│   │   └── fear_greed_index.csv           # Market sentiment dataset
│   │
│   └── processed/
│       ├── merged_trader_sentiment.csv    # Final merged dataset
│       ├── sentiment_metrics.csv          # Aggregated metrics
│       ├── side_performance.csv           # Long vs short analysis
│       └── top_accounts.csv               # Top traders by PnL

├── charts/
│   ├── total_pnl_by_sentiment.png         # Profit comparison
│   ├── avg_pnl_by_sentiment.png           # Avg PnL comparison
│   ├── win_rate_by_sentiment.png          # Win rate comparison
│   ├── trade_count_by_sentiment.png       # Activity analysis
│   ├── pnl_distribution_by_sentiment.png  # Distribution analysis
│   ├── leverage_by_sentiment.png          # Risk analysis
│   ├── trade_size_by_sentiment.png        # Trade size analysis
│   ├── side_pnl_by_sentiment.png          # Long vs short
│   └── top_accounts_by_pnl.png            # Top traders

├── reports/
│   └── summary_report.md                  # Final analysis report

├── main.py                                # Data processing & analysis pipeline
├── app.py                                 # Streamlit dashboard
├── requirements.txt                       # Dependencies
└── README.md                              # Project documentation
```

---

# ▶️ How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run data pipeline

```bash
python main.py
```

### 3. Launch dashboard

```bash
streamlit run app.py
```

---

# 📊 Key Insights

* Traders generate higher profits during **Greed phases**
* Win rate improves during **Fear periods**
* Extreme sentiment leads to:

  * Higher trading activity
  * Higher volatility
* Risk-taking (leverage) increases during optimistic markets

---

# 🔮 Future Improvements

* 📈 Add Sharpe ratio & risk-adjusted metrics
* ⏱ Time-based trend analysis (monthly/weekly)
* 🤖 Machine learning prediction model
* 🌐 Real-time API integration
* 📊 More advanced visualizations (heatmaps, correlations)
* 👤 User-specific trader analysis

---

# 🧠 Conclusion

This project demonstrates that:

* Market sentiment significantly impacts trading performance
* Trader behavior changes based on emotional market states
* Combining sentiment + trade data unlocks deeper insights

👉 Sentiment should not be used alone,
but it is a **powerful complementary signal** in trading strategy design.

---

# 👤 Author

**Madhura Gundluru**
GitHub name : **madhura276**

---

# ⭐ Final Note

This project represents an **end-to-end data analytics workflow**:

✔ Data Engineering
✔ Data Analysis
✔ Visualization
✔ Dashboard Development
✔ Deployment

---
