import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px

# ====================================================
# KONFIGURASI HALAMAN
# ====================================================
st.set_page_config(layout="wide")
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>',
    unsafe_allow_html=True
)

# ====================================================
# LOAD LOGO
# ====================================================
try:
    image = Image.open("Jenna-Logo.jpeg")
except FileNotFoundError:
    image = None
    st.warning("⚠️ File 'Jenna-Logo.jpeg' tidak ditemukan.")

# ====================================================
# LOAD DATA EXCEL
# ====================================================
try:
    df = pd.read_excel("penjualan-jenna.xlsx")
except FileNotFoundError:
    st.error("❌ File 'penjualan-jenna.xlsx' tidak ditemukan.")
    st.stop()

# ====================================================
# CLEAN & KONVERSI TANGGAL
# ====================================================
df.columns = df.columns.str.strip()
df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
df = df.dropna(subset=["Tanggal"])

# ====================================================
# SIDEBAR : LOGO + FILTER WAKTU
# ====================================================
if image:
    st.sidebar.image(image, width=200)

st.sidebar.markdown("---")
st.sidebar.header("⏱️ Filter Waktu")

mode_waktu = st.sidebar.selectbox(
    "Pilih Periode",
    ["Harian", "Mingguan", "Bulanan", "Tahunan"]
)

# ====================================================
# LOGIKA FILTER
# ====================================================
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

else:  # Tahunan
    tahun_pilih = st.sidebar.selectbox(
        "Pilih Tahun",
        sorted(df["Tanggal"].dt.year.unique())
    )
    df_filter = df[df["Tanggal"].dt.year == tahun_pilih]
    label_periode = f"Tahun {tahun_pilih}"

# ====================================================
# HEADER UTAMA
# ====================================================
col1, col2 = st.columns([0.12, 0.88])

with col1:
    if image:
        st.image(image, width=150)

with col2:
    st.markdown(
        "<center><h1>Penjualan Jenna Scent</h1></center>",
        unsafe_allow_html=True
    )

# ====================================================
# INFORMASI PERIODE
# ====================================================
st.markdown(f"### 📅 Periode Data:
