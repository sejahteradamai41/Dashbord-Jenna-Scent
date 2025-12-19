import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# ====================================================
# 1. LOAD LOGO
# ====================================================
try:
    image = Image.open("Jenna-Logo.jpeg")
except FileNotFoundError:
    st.warning("⚠️ File 'Jenna-Logo.jpeg' tidak ditemukan.")
    image = None

# ====================================================
# 2. LOAD DATA EXCEL
# ====================================================
try:
    df = pd.read_excel("penjualan-jenna.xlsx")
except FileNotFoundError:
    st.error("❌ File 'penjualan-jenna.xlsx' tidak ditemukan.")
    st.stop()

# ====================================================
# 3. FILTER WAKTU (HARIAN, MINGGUAN, BULANAN, TAHUNAN)
# ====================================================
# ====================================================
# 3. FILTER WAKTU (HARIAN, MINGGUAN, BULANAN, TAHUNAN)
# ====================================================
df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
df = df.dropna(subset=["Tanggal"])

st.sidebar.header("⏱️ Filter Waktu")

mode_waktu = st.sidebar.selectbox(
    "Pilih Periode",
    ["Harian", "Mingguan", "Bulanan", "Tahunan"]
)

if mode_waktu == "Harian":
    tanggal_pilih = st.sidebar.date_input(
        "Pilih Tanggal",
        df["Tanggal"].max().date()
    )
    df_filter = df[df["Tanggal"].dt.date == tanggal_pilih]
    label_periode = tanggal_pilih.strftime("%d %B %Y")

elif mode_waktu == "Mingguan":
    df["Minggu"] = df["Tanggal"].dt.to_period("W").astype(str)
    minggu_pilih = st.sidebar.selectbox(
        "Pilih Minggu",
        sorted(df["Minggu"].unique())
    )
    df_filter = df[df["Minggu"] == minggu_pilih]
    label_periode = f"Minggu {minggu_pilih}"

elif mode_waktu == "Bulanan":
    df["Bulan"] = df["Tanggal"].dt.to_period("M").astype(str)
    bulan_pilih = st.sidebar.selectbox(
        "Pilih Bulan",
        sorted(df["Bulan"].unique())
    )
    df_filter = df[df["Bulan"] == bulan_pilih]
    label_periode = bulan_pilih

elif mode_waktu == "Tahunan":
    tahun_pilih = st.sidebar.selectbox(
        "Pilih Tahun",
        sorted(df["Tanggal"].dt.year.unique())
    )
    df_filter = df[df["Tanggal"].dt.year == tahun_pilih]
    label_periode = f"Tahun {tahun_pilih}"

# ====================================================
# HEADER
# ====================================================
col1, col2 = st.columns([0.1, 0.9])

with col1:
    if image:
        st.image(image, width=200)

with col2:
    st.markdown(
        """
        <center><h1>Penjualan Jenna Scent</h1></center>
        """,
        unsafe_allow_html=True
    )

# ====================================================
# INFORMASI PERIODE
# ====================================================
col3, col4, col5 = st.columns([0.1, 0.45, 0.45])

with col3:
    st.write(f"Periode data:  \n **{label_periode}**")

# ====================================================
# BAR CHART – TOTAL QUANTITY PER VARIAN
# ====================================================
with col4:
    st.subheader("📊 Grafik Total Penjualan Per Varian")

    fig = px.bar(
        df_filter,
        x="Varian",
        y="Quantity",
        labels={"Quantity": "Jumlah Terjual"},
        title=f"Total Quantity Per Varian ({label_periode})",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📌 Detail Data Penjualan")
    data_barang = df_filter[[
        "No", "Tanggal", "Varian", "Quantity", "Harga Barang", "HPP", "Stok Barang"
    ]]
    st.dataframe(data_barang, use_container_width=True)

# ====================================================
# PIE CHART – VARIAN PALING LARIS
# ====================================================
with col5:
    st.subheader("🎯 Analisis Varian Paling Laris")

    varian_laris = df_filter.groupby("Varian")["Quantity"].sum().reset_index()

    fig_pie = px.pie(
        varian_laris,
        names="Varian",
        values="Quantity",
        title=f"Varian Parfum Paling Laris ({label_periode})",
        hole=0.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)
