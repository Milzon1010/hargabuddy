# app.py

import streamlit as st
import pandas as pd
from scrapper import scrape_tokopedia_graphql
from io import BytesIO

# 🧭 Setup halaman
st.set_page_config(page_title="Tokopedia Scraper Pro", layout="wide")
st.title("🛍️ HargaBuddy - Scraper Produk Tokopedia")
st.markdown("Temukan produk, filter harga, dan ekspor data ke Excel 💡\n")

# 📌 Input User
keyword = st.text_input("Masukkan keyword produk:", value="sepatu adidas")
start_page = st.number_input("Dari halaman", min_value=1, value=1, step=1)
end_page = st.number_input("Sampai halaman", min_value=start_page, value=start_page, step=1)

col1, col2 = st.columns(2)
with col1:
    min_price = st.number_input("Harga minimum (Rp)", min_value=0, value=0, step=5000)
with col2:
    max_price = st.number_input("Harga maksimum (Rp)", min_value=0, value=1000000, step=5000)

# 🔘 Tombol Action
if st.button("Cari Produk"):
    with st.spinner("🔄 Mengambil data dari Tokopedia..."):
        df = scrape_tokopedia_graphql(keyword, start_page, end_page, min_price, max_price)
        if not df.empty:
            st.success(f"✅ {len(df)} produk ditemukan.")
            df['Link'] = df['Link'].apply(lambda x: f"[🔗 Buka Link]({x})")
            st.markdown("### 📊 Hasil Pencarian Produk") 
            st.write(df.to_markdown(index=False), unsafe_allow_html=True)

            # 📥 Export ke Excel
            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="📥 Download Excel",
                data=buffer,
                file_name="tokopedia_products.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # 📊 Visualisasi Harga
            st.subheader("💸 Distribusi Harga Produk")
            st.bar_chart(df['Harga Numeric'])

            # 📍 Visualisasi Kota
            st.subheader("📍 Sebaran Produk Berdasarkan Kota")
            st.bar_chart(df['Kota'].value_counts())
        else:
            st.warning("Tidak ada produk ditemukan dengan filter tersebut.")
