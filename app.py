import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# ====================================================
# KONFIGURASI HALAMAN
# ====================================================
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# ====================================================
# LOAD LOGO
# ====================================================
try:
    image = Image.open("Jenna-Logo.jpeg")
except FileNotFoundError:
    image = None

# ====================================================
# LOAD DATA
# ====================================================
df = pd.read_excel("penjualan-jenna.xlsx")
df.columns = df.columns.str.strip()
df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
df = df.dropna(subset=["Tanggal"])

# ====================================================
# SIDEBAR : LOGO + FILTER
# ====================================================
if image:
    st.sidebar.image(image, width=200)

st.sidebar.markdown("---")
st.sidebar.header("⏱️ Filter Waktu")

mode_waktu = st.sidebar.selectbox(
    "Pilih Periode",
    ["Bulanan", "Tahunan", "Mingguan", "Harian"],
    index=0  # default BULANAN
)

# ====================================================
# FILTER LOGIC (DEFAULT OKTOBER 2024)
# ====================================================
df["Bulan"] = df["Tanggal"].dt.to_period("M").astype(str)
df["Tahun"] = df["Tanggal"].dt.year

if mode_waktu == "Bulanan":
    bulan_default = "2024-10"
    bulan_list = sorted(df["Bulan"].unique())
    bulan_pilih = st.sidebar.selectbox(
        "Pilih Bulan",
        bulan_list,
        index=bulan_list.index(bulan_default) if bulan_default in bulan_list else 0
    )
    df_filter = df[df["Bulan"] == bulan_pilih]
    label_periode = bulan_pilih

elif mode_waktu == "Tahunan":
    tahun_list = sorted(df["Tahun"].unique())
    tahun_pilih = st.sidebar.selectbox(
        "Pilih Tahun",
        tahun_list,
        index=tahun_list.index(2024) if 2024 in tahun_list else 0
    )
    df_filter = df[df["Tahun"] == tahun_pilih]
    label_periode = f"Tahun {tahun_pilih}"

elif mode_waktu == "Mingguan":
    df["Minggu"] = df["Tanggal"].dt.to_period("W").astype(str)
    minggu_pilih = st.sidebar.selectbox(
        "Pilih Minggu",
        sorted(df["Minggu"].unique())
    )
    df_filter = df[df["Minggu"] == minggu_pilih]
    label_periode = f"Minggu {minggu_pilih}"

else:  # Harian
    tanggal_pilih = st.sidebar.date_input(
        "Pilih Tanggal",
        df["Tanggal"].max().date()
    )
    df_filter = df[df["Tanggal"].dt.date == tanggal_pilih]
    label_periode = tanggal_pilih.strftime("%d %B %Y")

# ====================================================
# CEK DATA KOSONG
# ====================================================
if df_filter.empty:
    st.warning("⚠️ Tidak ada data untuk periode ini.")
    st.stop()

# ====================================================
# HEADER
# ====================================================
col1, col2 = st.columns([0.12, 0.88])

with col1:
    if image:
        st.image(image, width=150)

with col2:
    st.markdown("<center><h1>Penjualan Jenna Scent</h1></center>", unsafe_allow_html=True)

st.markdown(f"### 📅 Periode Data: **{label_periode}**")

# ====================================================
# KPI (IKUT FILTER)
# ====================================================
k0, k1, k2, k3, k4 = st.columns(5)

with k0:
    st.metric(
        "Total Terjual (Keseluruhan)",
        int(df["Quantity"].sum())
    )

with k1:
    st.metric("Total Terjual", int(df_filter["Quantity"].sum()))

with k2:
    st.metric("Jumlah Varian", df_filter["Varian"].nunique())

with k3:
    st.metric("Jumlah Aroma", df_filter["Aroma"].nunique() if "Aroma" in df_filter.columns else "—")

with k4:
    st.metric("Total Stok", int(df_filter["Stok Barang"].sum()))

# ====================================================
# BAR CHART
# ====================================================
st.markdown("## 📊 Total Penjualan per Varian")

varian_total = df_filter.groupby("Varian")["Quantity"].sum().reset_index()

fig_bar = px.bar(
    varian_total,
    x="Varian",
    y="Quantity",
    title="Total Penjualan per Varian"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ====================================================
# PIE VARIAN
# ====================================================
st.markdown("## ❤️ Varian Paling Disukai")

fig_varian = px.pie(
    varian_total,
    names="Varian",
    values="Quantity",
    hole=0.4
)
st.plotly_chart(fig_varian, use_container_width=True)

# ====================================================
# PIE AROMA
# ====================================================
if "Aroma" in df_filter.columns:
    st.markdown("## 🌸 Aroma Terlaris")

    aroma_laris = df_filter.groupby("Aroma")["Quantity"].sum().reset_index()

    fig_aroma = px.pie(
        aroma_laris,
        names="Aroma",
        values="Quantity",
        hole=0.4
    )
    st.plotly_chart(fig_aroma, use_container_width=True)

# ====================================================
# STOK & DATA
# ====================================================
st.markdown("## 📦 Ringkasan Stok Barang")
stok_df = df_filter.groupby("Varian")["Stok Barang"].sum().reset_index()
st.dataframe(stok_df, use_container_width=True)

st.markdown("## 📋 Data Lengkap Penjualan")
st.dataframe(df_filter, use_container_width=True)
