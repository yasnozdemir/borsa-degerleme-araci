import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Stock FutureSight Pro", layout="wide")

# Tasarım - Görseldeki Koyu Tema
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .scenario-card {
        background-color: #1c1f26; padding: 20px;
        border-radius: 12px; margin-bottom: 15px;
        border-left: 6px solid #3d4450; color: white;
    }
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
        
        # Sidebar Girişleri
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
            st.markdown(f"<div class='metric-value'>${current_price:.2f}</div>", unsafe_allow_html=True)
            
            st.write("### Price Level Visualization")
            # --- HATASIZ GRAFİK ---
            fig = go.Figure()
            scenarios = ['High', 'Mid', 'Low', 'Current']
            values = [high_val, mid_val, low_val, current_price]
            colors = ['#00e5ff', '#9d4edd', '#ff9100', '#6c757d']
            
            fig.add_trace(go.Bar(
                y=scenarios,
                x=values,
                orientation='h',
                marker=dict(color=colors),
                text=[f"${v:.2f}" for v in values],
                textposition='outside'
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(tickfont=dict(color="white")),
                margin=dict(l=10, r=50, t=10, b=10),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("### 2-Year Scenarios")
            for name, val, color in [("Low", low_val, "#ff9100"), ("Mid", mid_val, "#9d4edd"), ("High", high_val, "#00e5ff")]:
                upside = ((val / current_price) - 1) * 100
                st.markdown(f"""
                    <div class="scenario-card" style="border-left-color: {color};">
                        <div style="display: flex; justify-content: space-between;">
                            <b>{name} Case</b> <b>${val:.2f}</b>
                        </div>
                        <div style="text-align: right; color: {'#00ff00' if upside > 0 else '#ff4b4b'};">
                            {'↑' if upside > 0 else '↓'} {abs(upside):.2f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Hata: {e}")
