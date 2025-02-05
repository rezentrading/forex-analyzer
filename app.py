import streamlit as st
import pandas as pd
import plotly.express as px

# 예제 데이터 (FXCM API 연동 시 실제 데이터 사용)
data = {
    'Currency Pair': ['GBP/USD', 'EUR/USD'],
    'Fri 12:00 Price': [1.3000, 1.1000],
    'Fri 12:30 Price': [1.3050, 1.1020],
    'Fri 21:59 Price': [1.3100, 1.1050],
    'Sun 22:03 Price': [1.3150, 1.1080]
}

df = pd.DataFrame(data)

# 가격 차이 및 변동률 계산
df['12:00 vs 12:30 Diff'] = df['Fri 12:30 Price'] - df['Fri 12:00 Price']
df['12:00 vs 12:30 % Change'] = (df['12:00 vs 12:30 Diff'] / df['Fri 12:00 Price']) * 100
df['21:59 vs 22:03 Diff'] = df['Sun 22:03 Price'] - df['Fri 21:59 Price']
df['21:59 vs 22:03 % Change'] = (df['21:59 vs 22:03 Diff'] / df['Fri 21:59 Price']) * 100

# Streamlit UI
st.title("FOREX Market Analyzer")
st.write("## GBP/USD & EUR/USD Market Overview")

# 표 표시
st.table(df)

# 차트 생성
fig = px.line(df, x='Currency Pair', y=['Fri 12:00 Price', 'Fri 12:30 Price', 'Fri 21:59 Price', 'Sun 22:03 Price'],
              title='Price Changes Over Specified Time Intervals')
st.plotly_chart(fig)

# 경고 표시
max_diff_pair = df.loc[df['21:59 vs 22:03 Diff'].idxmax(), 'Currency Pair']
st.warning(f'⚠️ {max_diff_pair} has the largest price difference between Fri 21:59 and Sun 22:03.')
