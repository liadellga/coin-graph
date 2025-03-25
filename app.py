import streamlit as st
import pyupbit
import pandas as pd

coin_list = [coin for coin in pyupbit.get_tickers(fiat="KRW")][:10]
selected_coin = st.selectbox("코인을 선택하세요", coin_list)

# interval 선택
interval_options = {
    "1분": "minute1",
    "5분": "minute5",
    "15분": "minute15",
    "1시간": "minute60",
    "4시간": "minute240",
    "일봉": "day",
    "주봉": "week",
    "월봉": "month"
}
interval_label = st.selectbox("Interval 선택", list(interval_options.keys()))
interval = interval_options[interval_label]

if "minute" in interval:
    slider_label = f"{interval_label} 기준 데이터 수 (최대 200)"
    max_val = 200
elif interval == "day":
    slider_label = "몇 일치의 데이터를 볼까요?"
    max_val = 90
elif interval == "week":
    slider_label = "몇 주치의 데이터를 볼까요?"
    max_val = 60
elif interval == "month":
    slider_label = "몇 개월치의 데이터를 볼까요?"
    max_val = 24
else:
    slider_label = "조회할 데이터 수"
    max_val = 100

count = st.slider(slider_label, min_value=10, max_value=max_val, value=min(30, max_val))

if "minute" not in interval:
    st.write(f"{count}, {interval}")
else:
    n= int(interval.split("minute")[1])
    st.write(f"{count * n} min ")

df = pyupbit.get_ohlcv(selected_coin, interval=interval, count=count)
df = df.reset_index()
df = df[["index", "close"]]
df.columns = ["날짜", "종가"]

st.line_chart(df.set_index("날짜")["종가"])