import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# ====================================================
# 1. LOAD LOGO
# Pastikan file namanya persis: Jenna-Logo.jpeg
# ====================================================
try:
    image = Image.open("Jenna-Logo.jpeg")
except FileNotFoundError:
    st.warning("⚠️ File 'Jenna-Logo.jpeg' tidak ditemukan. Pastikan file berada 1 folder dengan app.py")
    image = None

# ====================================================
# 2. LOAD DATA EXCEL
# Pastikan nama file persis: penjualan -jenna.xlsx
# ====================================================
try:
    df = pd.read_excel("penjualan -jenna.xlsx")
except FileNotFoundError:
    st.error("❌ File 'penjualan -jenna.xlsx' tidak ditemukan. Pastikan berada 1 folder dengan app.py")
    st.stop()

# ====================================================
# HEADER
# ====================================================
col1, col2 = st.columns([0.1, 0.9])

with col1:
    if image:
        st.image(image, width=100)

with col2:
    st.markdown(
        """
        <style>
        .title-test {
            font-weight:bold;
            padding:5px;
            border-radius:6px;
        }
        </style>
        <center><h1 class="title-test">Penjualan Jenna Scent</h1></center>
        """,
        unsafe_allow_html=True
    )

# ====================================================
# INFORMASI TANGGAL UPDATE
# ====================================================
col3, col4, col5 = st.columns([0.1, 0.45, 0.45])

with col3:
    tanggal = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"Last updated:  \n **{tanggal}**")

# ====================================================
# BAR CHART – TOTAL QUANTITY PER VARIAN
# ====================================================
with col4:
    st.subheader("📊 Grafik Total Penjualan per Varian")

    fig = px.bar(
        df,
        x="Varian",
        y="Quantity",
        labels={"Quantity": "Jumlah Terjual"},
        title="Total Quantity per Varian",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # === TABEL DETAIL BARANG ===
    st.subheader("📌 Detail Data Penjualan")
    data_barang = df[[
        "No", "Tanggal", "Varian", "Quantity", "Harga Barang", "HPP", "Stok Barang"
    ]]
    st.dataframe(data_barang, use_container_width=True)

# ====================================================
# PIE CHART – VARIAN PALING LARIS
# ====================================================
with col5:
    st.subheader("🎯 Analisis Varian Paling Laris")

    varian_laris = df.groupby("Varian")["Quantity"].sum().reset_index()

    fig_pie = px.pie(
        varian_laris,
        names="Varian",
        values="Quantity",
        title="Varian Parfum Paling Laris",
        hole=0.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)
