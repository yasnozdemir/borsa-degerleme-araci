import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Sayfa yapılandırması
st.set_page_config(page_title="Stock FutureSight Pro", layout="wide")

# CSS ile Görseldeki Koyu Temayı Yakalayalım
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00d4ff; }
    .scenario-card {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 6px solid #3d4450;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Stock FutureSight")

# Sol Panel (Sidebar)
st.sidebar.header("Parametreler")
ticker = st.sidebar.text_input("Hisse Kodu:", "GOOGL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('currentPrice', 0.0)
        
        # Finansal Veriler
        forward_eps = info.get('forwardEps', 1.0)
        
        st.sidebar.divider()
        st.sidebar.write("2-Year-Ahead P/E Ratios")
        low_pe = st.sidebar.number_input("Low", value=15.3)
        mid_pe = st.sidebar.number_input("Mid", value=18.4)
        high_pe = st.sidebar.number_input("High", value=21.8)
        
        growth = st.sidebar.slider("Yıllık Büyüme Beklentisi (%)", 0, 100, 15)
        # 2 yıllık büyüme faktörü
        projected_eps = forward_eps * ((1 + growth/100) ** 2)

        # Senaryo Hesaplamaları
        low_val = projected_eps * low_pe
        mid_val = projected_eps * mid_pe
        high_val = projected_eps * high_pe

        # ANA EKRAN TASARIMI
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader(f"Valuation Summary for {ticker}")
            st.write("Projected 2-year valuation based on your inputs.")
            st.metric("Calculated Current Price", f"${current_price:.2f}")
            
            # Fiyat Seviyesi Grafiği (Price Level Visualization)
            st.write("### Price Level Visualization")
            fig = go.Figure()
            
            # Yatay Çubuklar
            scenarios = ['High', 'Mid', 'Low', 'Current']
            values = [high_val, mid_val, low_val, current_price]
            colors = ['#00e5ff', '#9d4edd', '#ff9100', '#6c757d']
            
            fig.add_trace(go.Bar(
                y=scenarios,
                x=values,
                orientation='h',
                marker=dict(color=colors, line=dict(width=0)),
                width=0.6
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, font=dict(color="white")),
                yaxis=dict(font=dict(color="white")),
                height=300,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("### 2-Year Scenarios")
            
            def scenario_box(name, price, color):
                upside = ((price / current_price) - 1) * 100
                st.markdown(f"""
                    <div class="scenario-card" style="border-left-color: {color};">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #aeb4be; font-weight: bold;">{name} Case</span>
                            <span style="color: white; font-weight: bold;">${price:.2f}</span>
                        </div>
                        <div style="text-align: right; color: {'#00ff00' if upside > 0 else '#ff4b4b'}; font-size: 14px;">
                            {'↑' if upside > 0 else '↓'} {abs(upside):.2f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            scenario_box("Low", low_val, "#ff9100")
            scenario_box("Mid", mid_val, "#9d4edd")
            scenario_box("High", high_val, "#00e5ff")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
