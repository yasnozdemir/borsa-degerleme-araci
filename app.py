import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="Stock FutureSight Pro", layout="wide")

# Tasarım - Koyu Tema Dokunuşu
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2227; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Stock FutureSight: Senaryo Analizi")

# Sidebar - Girişler
st.sidebar.header("🔍 Şirket Seçimi")
ticker_symbol = st.sidebar.text_input("Ticker (Hisse Kodu):", "GOOGL").upper()

if ticker_symbol:
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        current_price = info.get('currentPrice', 1)
        
        # Finansal Verileri Çekme (CFO ve EPS)
        cash_flow = stock.cashflow
        # En son Operasyonel Nakit Akışı (CFO)
        latest_cfo = cash_flow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cash_flow.index else 0
        shares_outstanding = info.get('sharesOutstanding', 1)
        cfo_per_share = latest_cfo / shares_outstanding
        forward_eps = info.get('forwardEps', 1)

        st.sidebar.divider()
        st.sidebar.header("⚙️ Senaryo Parametreleri")
        val_metric = st.sidebar.selectbox("Değerleme Metriği:", ["Forward EPS", "CFO Per Share"])
        base_val = forward_eps if val_metric == "Forward EPS" else cfo_per_share
        
        # Çarpan Girişleri (Görseldeki gibi)
        st.sidebar.write(f"2 Yıllık {val_metric} Çarpanları:")
        low_mult = st.sidebar.number_input("Low (Kötü)", value=15.0)
        mid_mult = st.sidebar.number_input("Mid (Normal)", value=18.4)
        high_mult = st.sidebar.number_input("High (İyi)", value=21.8)
        
        # 2 Yıllık Tahmini Büyüme (Yıllık %10 varsayılan)
        growth_rate = st.sidebar.slider("Yıllık Tahmini Büyüme (%)", 0, 50, 10) / 100
        projected_val = base_val * ((1 + growth_rate) ** 2)

        # HESAPLAMALAR
        low_target = projected_val * low_mult
        mid_target = projected_val * mid_mult
        high_target = projected_val * high_mult

        # ANA PANEL
        col_main1, col_main2 = st.columns([1, 1.5])

        with col_main1:
            st.subheader(f"Valuation Summary for {ticker_symbol}")
            st.write(f"Seçilen Metrik: {val_metric}")
            st.metric("Mevcut Fiyat", f"${current_price:.2
