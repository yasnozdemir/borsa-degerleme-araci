import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Sayfa Yapılandırması
st.set_page_config(page_title="Hisse Gelecek Analizi Pro", layout="wide")

# Tasarım - Koyu Tema ve Stil Ayarları
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

st.title("📊 Hisse Değerleme ve Senaryo Analizi")

# Yan Panel (Parametreler)
st.sidebar.header("⚙️ Analiz Ayarları")
ticker = st.sidebar.text_input("Hisse Kodu (Örn: AAPL, NVDA):", "GOOGL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        guncel_fiyat = info.get('currentPrice', 1.0)
        beklenen_eps = info.get('forwardEps', 1.0)
        
        # Yan Panel Girişleri
        st.sidebar.write("### 2 Yıllık Tahmini F/K Çarpanları")
        low_pe = st.sidebar.number_input("Düşük (Ayı Senaryosu)", value=15.0)
        mid_pe = st.sidebar.number_input("Orta (Baz Senaryo)", value=18.5)
        high_pe = st.sidebar.number_input("Yüksek (Boğa Senaryosu)", value=22.0)
        
        buyume_orani = st.sidebar.slider("Yıllık Tahmini Kâr Büyümesi (%)", 0, 100, 15)
        
        # Hesaplamalar (Bileşik Büyüme Formülü)
        # Formül: 2 Yıl Sonraki EPS = Mevcut Beklenen EPS * (1 + Büyüme)^2
        gelecek_eps = beklenen_eps * ((1 + buyume_orani/100) ** 2)
        
        dusuk_hedef = gelecek_eps * low_pe
        orta_hedef = gelecek_eps * mid_pe
        yuksek_hedef = gelecek_eps * high_pe

        # ANA EKRAN
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"### {ticker} Değerleme Özeti")
            st.markdown(f"**Hesaplanan Güncel Fiyat:**")
            st.markdown(f"<div class='metric-value'>${guncel_fiyat:.2f}</div>", unsafe_allow_html=True)
            
            st.write("### Fiyat Seviyesi Görselleştirmesi")
            # --- GRAFİK ---
            fig = go.Figure()
            senaryolar = ['Yüksek', 'Orta', 'Düşük', 'Güncel']
            degerler = [yuksek_hedef, orta_hedef, dusuk_hedef, guncel_fiyat]
            renkler = ['#00e5ff', '#9d4edd', '#ff9100', '#6c757d']
            
            fig.add_trace(go.Bar(
                y=senaryolar,
                x=degerler,
                orientation='h',
                marker=dict(color=renkler),
                text=[f"${v:.2f}" for v in degerler],
                textposition='outside',
                textfont=dict(color='white')
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(tickfont=dict(color="white", size=14)),
                margin=dict(l=10, r=60, t=10, b=10),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("### 2 Yıllık Gelecek Senaryoları")
            for isim, deger, renk in [("Düşük", dusuk_hedef, "#ff9100"), 
                                     ("Orta", orta_hedef, "#9d4edd"), 
                                     ("Yüksek", yuksek_hedef, "#00e5ff")]:
                potansiyel = ((deger / guncel_fiyat) - 1) * 100
                st.markdown(f"""
                    <div class="scenario-card" style="border-left-color: {renk};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: bold; font-size: 18px;">{isim} Senaryo</span>
                            <span style="font-size: 20px; font-weight: bold;">${deger:.2f}</span>
                        </div>
                        <div style="text-align: right; color: {'#00ff00' if potansiyel > 0 else '#ff4b4b'}; font-weight: bold; margin-top: 5px;">
                            {'↑' if potansiyel > 0 else '↓'} %{abs(potansiyel):.2f} Getiri Potansiyeli
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Veri çekme veya hesaplama hatası: {e}")
