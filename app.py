import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Stock FutureSight Pro", layout="wide")

# Görseldeki Tasarım İçin CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .scenario-card {
        background-color: #1c1f26; padding: 20px;
        border-radius: 12px; margin-bottom: 15px;
        border-left: 6px solid #3d4450; color: white;
    }
    .metric-title { color: #aeb4be; font-size: 16px; }
    .metric-value { color: #00d4ff; font-size: 32px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.header("Parametreler")
ticker = st.sidebar.text_input("Hisse Kodu:", "GOOGL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('currentPrice', 1.0)
        forward_eps = info.get('forwardEps', 1.0)
        
        # Sidebar Girişleri (Görseldeki Çarpanlar)
        st.sidebar.write("2-Year-Ahead P/E Ratios")
        low_pe = st.sidebar.number_input("Low", value=15.3)
        mid_pe = st.sidebar.number_input("Mid", value=18.4)
        high_pe = st.sidebar.number_input("High", value=21.8)
        growth = st.sidebar.slider("Yıllık Büyüme (%)", 0, 100, 15)
        
        # Hesaplamalar
        projected_eps = forward_eps * ((1 + growth/100) ** 2)
        low_val = projected_eps * low_pe
        mid_val = projected_eps * mid_pe
        high_val = projected_eps * high_pe

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"### Valuation Summary for {ticker}")
            st.markdown(f"<div class='metric-title'>Calculated Current Price</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>${current_price:.2f}</div>", unsafe_allow_html=True)
            
            st.write("### Price Level Visualization")
            # --- HATA DÜZELTİLMİŞ GRAFİK ALANI ---
            fig = go.Figure()
            
            scenarios = ['High', 'Mid', 'Low', 'Current']
            values = [high_val, mid_val, low_val, current_price]
            colors = ['#00e5ff', '#9d4edd', '#ff9100', '#6c757d']
            
            fig.add_trace(go.Bar(
                y=scenarios,
                x=values,
                orientation='h',
                marker=dict(color=colors),
                width=0.6,
                text=[f"${v:.2f}" for v in values],
                textposition='outside',
                textfont=dict(color='white')
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(tickfont=dict(color="white", size=14)),
                height=350,
                margin=dict(l=10, r=50, t=10, b=10)
            )
            st.plotly_chart(fig, use_
