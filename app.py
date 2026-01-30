import streamlit as st
import yfinance as yf

st.title("🇺🇸 ABD Borsası Değerleme Aracı")
st.write("Şirket kâr tahminleri ve çarpanlara göre fiyat analizi.")

# 1. Kullanıcı Girişi
ticker = st.text_input("Hisse Kodunu Giriniz (Örn: AAPL, MSFT):", "AAPL").upper()
target_pe = st.slider("Hedef F/K (P/E) Çarpanı Seçin:", 5, 50, 20)

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 2. Veri Çekme
        current_price = info.get('currentPrice', 0)
        forward_eps = info.get('forwardEps', 0)
        company_name = info.get('longName', 'Bilinmeyen Şirket')
        
        st.subheader(f"{company_name} Analizi")
        
        # 3. Hesaplama
        # Formül: Tahmini Değer = Beklenen Hisse Başı Kâr * Hedef Çarpan
        estimated_value = forward_eps * target_pe
        upside = ((estimated_value / current_price) - 1) * 100
        
        # 4. Arayüzde Gösterme
        col1, col2, col3 = st.columns(3)
        col1.metric("Güncel Fiyat", f"${current_price}")
        col2.metric("Beklenen EPS (1Y)", f"${forward_eps}")
        col3.metric("Tahmini Değer", f"${estimated_value:.2f}")

        if upside > 0:
            st.success(f"Potansiyel Getiri: %{upside:.2f}")
        else:
            st.error(f"Potansiyel Kayıp/Aşırı Değerleme: %{upside:.2f}")
            
    except Exception as e:
        st.error(f"Veri çekilirken bir hata oluştu. Ticker'ı kontrol edin. Hata: {e}")

st.info("Not: Bu araç sadece matematiksel bir tahmindir, yatırım tavsiyesi değildir.")
