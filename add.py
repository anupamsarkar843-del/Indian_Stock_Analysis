import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="NSE Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.title{
    font-size:40px;
    font-weight:bold;
    color:#1f77b4;
    text-align:center;
}

.subtitle{
    font-size:18px;
    color:gray;
    text-align:center;
}

.metric{
    background-color:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.markdown("<p class='title'>📈 NSE Stock Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Interactive Stock Price Visualization</p>", unsafe_allow_html=True)

st.write("")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Stocks_Nse.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📌 Filter Stocks")

category = st.sidebar.selectbox(
    "Select Category",
    sorted(df["Category"].unique())
)

category_df = df[df["Category"] == category]

stock = st.sidebar.selectbox(
    "Select Stock",
    sorted(category_df["Stock"].unique())
)

stock_df = category_df[category_df["Stock"] == stock]

# -----------------------------
# Date Filter
# -----------------------------
min_date = stock_df["Date"].min()
max_date = stock_df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

if len(date_range) == 2:
    start_date, end_date = date_range
    stock_df = stock_df[
        (stock_df["Date"] >= pd.to_datetime(start_date)) &
        (stock_df["Date"] <= pd.to_datetime(end_date))
    ]

# -----------------------------
# Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Latest Close",
    f"₹ {stock_df['Close'].iloc[-1]:.2f}"
)

col2.metric(
    "Highest Price",
    f"₹ {stock_df['Close'].max():.2f}"
)

col3.metric(
    "Lowest Price",
    f"₹ {stock_df['Close'].min():.2f}"
)

st.write("")

# -----------------------------
# Moving Average
# -----------------------------
stock_df = stock_df.sort_values("Date")
stock_df["MA20"] = stock_df["Close"].rolling(20).mean()

# -----------------------------
# Interactive Chart
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=stock_df["Date"],
        y=stock_df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="royalblue", width=3)
    )
)

fig.add_trace(
    go.Scatter(
        x=stock_df["Date"],
        y=stock_df["MA20"],
        mode="lines",
        name="20-Day MA",
        line=dict(color="orange", dash="dash")
    )
)

fig.update_layout(
    title=f"{stock} Stock Price",
    xaxis_title="Date",
    yaxis_title="Closing Price",
    template="plotly_white",
    hovermode="x unified",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Statistics
# -----------------------------
st.subheader("📊 Stock Statistics")

st.dataframe(stock_df.describe(), use_container_width=True)

# -----------------------------
# Dataset Preview
# -----------------------------
with st.expander("📄 View Dataset"):
    st.dataframe(stock_df, use_container_width=True)

# -----------------------------
# Download Button
# -----------------------------
csv = stock_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    file_name=f"{stock}.csv",
    mime="text/csv"
)
