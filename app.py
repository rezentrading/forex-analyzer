import requests

# FMP API 키 설정
FMP_API_KEY = "EXq8ysjulWcYBreTFdLc7G2PDAv8RW4R"  # 여기에 본인의 API 키 입력
BASE_URL = "https://financialmodelingprep.com/api/v3/quote/"

# GBP/USD & EUR/USD 실시간 환율 가져오는 함수
def get_forex_price(pair):
    url = f"{BASE_URL}{pair}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and len(data) > 0:
        return data[0]["price"]  # 실시간 가격 반환
    else:
        print(f"❌ FMP API 요청 실패: {response.status_code}")
        return None

# GBP/USD & EUR/USD 가격 확인
gbp_price = get_forex_price("GBPUSD")
eur_price = get_forex_price("EURUSD")

print(f"GBP/USD 가격: {gbp_price}")
print(f"EUR/USD 가격: {eur_price}")

import streamlit as st
import pandas as pd
import plotly.express as px

# 실시간 데이터 가져오기
gbp_price = get_forex_price("GBPUSD")
eur_price = get_forex_price("EURUSD")

# 예제 데이터 (시간별 시가 데이터 가정)
data = {
    'Currency Pair': ['GBP/USD', 'EUR/USD'],
    'Fri 12:00 Price': [gbp_price - 0.005, eur_price - 0.002],  
    'Fri 12:30 Price': [gbp_price - 0.003, eur_price - 0.001],
    'Fri 21:59 Price': [gbp_price - 0.002, eur_price - 0.0015],
    'Sun 22:03 Price': [gbp_price, eur_price]
}

df = pd.DataFrame(data)

# 가격 차이 및 변동률 계산
df['12:00 vs 12:30 Diff'] = df['Fri 12:30 Price'] - df['Fri 12:00 Price']
df['12:00 vs 12:30 % Change'] = (df['12:00 vs 12:30 Diff'] / df['Fri 12:00 Price']) * 100
df['21:59 vs 22:03 Diff'] = df['Sun 22:03 Price'] - df['Fri 21:59 Price']
df['21:59 vs 22:03 % Change'] = (df['21:59 vs 22:03 Diff'] / df['Fri 21:59 Price']) * 100

# Streamlit UI
st.title("FOREX Market Analyzer (FMP API 연동)")
st.write("## 실시간 GBP/USD & EUR/USD 데이터")

# 표 표시
st.table(df)

# 차트 생성
fig = px.bar(df, x='Currency Pair', 
             y=['Fri 12:00 Price', 'Fri 12:30 Price', 'Fri 21:59 Price', 'Sun 22:03 Price'],
             title='Price Comparison Across Different Time Points',
             barmode='stack')

st.plotly_chart(fig)



# 경고 표시 (21:59 vs 22:03 중 변동폭이 큰 통화 강조)
max_diff_pair = df.loc[df['21:59 vs 22:03 Diff'].idxmax(), 'Currency Pair']
st.warning(f'⚠️ {max_diff_pair} has the largest price difference between Fri 21:59 and Sun 22:03.')

