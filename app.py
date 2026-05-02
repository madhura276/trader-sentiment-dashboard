import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Trader Sentiment Dashboard",
    layout="wide"
)

st.title("📊 Trader Performance vs Market Sentiment")
st.markdown("### 📊 Real-Time Trading Analytics Dashboard")

# =========================
# LOAD DATA
# =========================
DATA_PATH = "data/processed/merged_trader_sentiment.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

sentiments = st.sidebar.multiselect(
    "Select Sentiment",
    options=sorted(df["classification"].dropna().unique()),
    default=sorted(df["classification"].dropna().unique())
)

filtered_df = df[df["classification"].isin(sentiments)]

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Performance", "🧠 Insights"])

# =========================
# TAB 1: OVERVIEW
# =========================
with tab1:

    st.subheader("📈 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trades", f"{len(filtered_df):,}")
    col2.metric("Total PnL", f"{filtered_df['closed_pnl'].sum():,.2f}")
    col3.metric("Avg PnL", f"{filtered_df['closed_pnl'].mean():,.2f}")
    col4.metric("Win Rate", f"{(filtered_df['closed_pnl'] > 0).mean() * 100:.2f}%")

    # Best sentiment
    if not filtered_df.empty:
        best_sentiment = filtered_df.groupby("classification")["closed_pnl"].sum().idxmax()
        st.metric("🏆 Best Sentiment", best_sentiment)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Total PnL by Sentiment")

        pnl_df = filtered_df.groupby("classification")["closed_pnl"].sum().reset_index()

        fig1 = px.bar(
            pnl_df,
            x="classification",
            y="closed_pnl",
            color="classification",
            text_auto=True
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("📊 Average PnL by Sentiment")

        avg_df = filtered_df.groupby("classification")["closed_pnl"].mean().reset_index()

        fig2 = px.bar(
            avg_df,
            x="classification",
            y="closed_pnl",
            color="classification",
            text_auto=True
        )

        st.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 2: PERFORMANCE
# =========================
with tab2:

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📉 PnL Distribution")

        fig3 = px.histogram(
            filtered_df,
            x="closed_pnl",
            color="classification",
            nbins=50
        )

        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("📊 Win Rate by Sentiment")

        win_df = filtered_df.copy()
        win_df["is_win"] = win_df["closed_pnl"] > 0

        win_rate_df = win_df.groupby("classification")["is_win"].mean().reset_index()

        fig4 = px.bar(
            win_rate_df,
            x="classification",
            y="is_win",
            color="classification",
            text_auto=".2f"
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # Cumulative PnL (WOW chart)
    st.subheader("📈 Cumulative PnL Over Time")

    if not filtered_df.empty:
        cum_df = filtered_df.sort_values("date").copy()
        cum_df["cumulative_pnl"] = cum_df["closed_pnl"].cumsum()

        fig5 = px.line(
            cum_df,
            x="date",
            y="cumulative_pnl"
        )

        st.plotly_chart(fig5, use_container_width=True)

# =========================
# TAB 3: INSIGHTS + TABLES
# =========================
with tab3:

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("🏆 Top Accounts")

        if "account" in filtered_df.columns:
            top_accounts = (
                filtered_df.groupby("account")["closed_pnl"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            st.dataframe(top_accounts, use_container_width=True)
        else:
            st.info("Account column not available")

    with col6:
        st.subheader("💰 Most Traded Coins")

        if "coin" in filtered_df.columns:
            top_coins = (
                filtered_df["coin"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            top_coins.columns = ["Coin", "Trade Count"]

            st.dataframe(top_coins, use_container_width=True)
        else:
            st.info("Coin column not available")

    st.divider()

    st.subheader("🧠 Key Insights")

    st.markdown("""
    - Traders tend to generate higher profits during **Greed** phases.
    - **Win rate improves during Fear**, indicating more cautious trading.
    - Extreme sentiment leads to **higher volatility and trading activity**.
    - Sentiment is useful but should be combined with other indicators.
    """)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Built with Streamlit • Sentiment-Based Trading Analysis")