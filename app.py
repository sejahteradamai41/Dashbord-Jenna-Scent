import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# ====================================================
# PAGE CONFIG
# ====================================================
st.set_page_config(
    page_title="Dashboard Penjualan Jenna Scent",
    layout="wide"
)

# ====================================================
# SIDEBAR – THEME & MODE
# ====================================================
st.sidebar.header("⚙️ Pengaturan Dashboard")

tema = st.sidebar.radio(
    "🎨 Tema Tampilan",
    ["Dark Mode", "Light Mode"],
    index=0
)

mode_tampilan = st.sidebar.selectbox(
    "🧩 Mode Tampilan",
    ["Sidang", "Laporan"]
)

# ====================================================
# THEME STYLE
# ====================================================
if tema == "Dark Mode":
    bg_color = "#0f172a"
    card_color = "#111827"
    text_color = "#e5e7eb"
    sub_text = "#9ca3af"
else:
    bg_color = "#f8fafc"
    card_color = "#ffffff"
    text_color = "#111827"
    sub_text = "#6b7280"

st.markdown(
    f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .kpi-card {{
        background-color: {card_color};
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ====================================================
# LOAD LOGO
# ====================================================
try:
    logo = Image.open("Jenna-Logo.jpeg")
except:
    logo = None

# ====================================================
# LOAD DATA
# ====================================================
df = pd.read_excel("penjualan-jenna.xlsx")
df.columns = df.columns.str.strip()
df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
df = df.dropna(subset=["Tanggal"])

df["Bulan"] = df["Tanggal"].dt.to_period("M").astype(str)
df["Tahun"] = df["Tanggal"].dt.year
df["Minggu"] = df["Tanggal"].dt.to_period("W").astype(str)

# ====================================================
# SIDEBAR – FILTER WAKTU
# ====================================================
st.sidebar.markdown("---")
st.sidebar.header("⏱️ Filter Waktu")

mode_waktu = st.sidebar.selectbox(
    "Pilih Periode",
    ["Harian", "Mingguan", "Bulanan", "Tahunan"]
)

if mode_waktu == "Harian":
    tanggal = st.sidebar.date_input("Pilih Tanggal", df["Tanggal"].max().date())
    df_filter = df[df["Tanggal"].dt.date == tanggal]
    label_periode = tanggal.strftime("%d %B %Y")

elif mode_waktu == "Mingguan":
    minggu = st.sidebar.selectbox("Pilih Minggu", sorted(df["Minggu"].unique()))
    df_filter = df[df["Minggu"] == minggu]
    label_periode = f"Minggu {minggu}"

elif mode_waktu == "Bulanan":
    bulan = st.sidebar.selectbox("Pilih Bulan", sorted(df["Bulan"].unique()))
    df_filter = df[df["Bulan"] == bulan]
    label_periode = bulan

else:
    tahun = st.sidebar.selectbox("Pilih Tahun", sorted(df["Tahun"].unique()))
    df_filter = df[df["Tahun"] == tahun]
    label_periode = f"Tahun {tahun}"

if df_filter.empty:
    st.warning("⚠️ Tidak ada data pada periode ini.")
    st.stop()

# ====================================================
# HEADER
# ====================================================
col1, col2 = st.columns([0.12, 0.88])
with col1:
    if logo:
        st.image(logo, width=200)

with col2:
    st.markdown(
        """
        <div style='text-align:center'>
            <h1 style='margin-bottom:0'>📊 Dashboard Penjualan</h1>
            <h3 style='font-weight:400; color:gray; margin-top:5px'>
                Jenna Scent
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    f"""
    <div style='
        display:inline-block;
        padding:6px 16px;
        border-radius:20px;
        background:#1f2937;
        color:white;
        margin-bottom:12px;
        font-size:14px;
    '>
        ⏱️ {mode_waktu} • {label_periode}
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Ringkasan performa penjualan berdasarkan periode yang dipilih")

# ====================================================
# KPI FUNCTION
# ====================================================
def kpi(title, value, subtitle=""):
    st.markdown(
        f"""
        <div class='kpi-card'>
            <h4>{title}</h4>
            <h1>{value}</h1>
            <span style='color:{sub_text}'>{subtitle}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ====================================================
# KPI SECTION
# ====================================================
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    kpi("Total Terjual", int(df_filter["Quantity"].sum()), "Periode terpilih")

with k2:
    kpi("Jumlah Varian", df_filter["Varian"].nunique())

with k3:
    kpi("Jumlah Aroma", df_filter["Aroma"].nunique() if "Aroma" in df_filter.columns else "-")

with k4:
    kpi("Total Stok", int(df_filter["Stok Barang"].sum()))

with k5:
    kpi("Total Transaksi", len(df_filter))

# ====================================================
# CHART – VARIAN
# ====================================================
st.markdown("## 📊 Total Penjualan per Varian")
varian_total = df_filter.groupby("Varian")["Quantity"].sum().reset_index()

fig_bar = px.bar(
    varian_total,
    x="Varian",
    y="Quantity",
    text_auto=True
)
st.plotly_chart(fig_bar, use_container_width=True)

# ====================================================
# PIE – VARIAN & AROMA
# ====================================================
c1, c2 = st.columns(2)

with c1:
    fig_varian = px.pie(varian_total, names="Varian", values="Quantity", hole=0.4)
    st.plotly_chart(fig_varian, use_container_width=True)

with c2:
    if "Aroma" in df_filter.columns:
        aroma_total = df_filter.groupby("Aroma")["Quantity"].sum().reset_index()
        fig_aroma = px.pie(aroma_total, names="Aroma", values="Quantity", hole=0.4)
        st.plotly_chart(fig_aroma, use_container_width=True)

# ====================================================
# DETAIL DATA (MODE LAPORAN)
# ====================================================
if mode_tampilan == "Laporan":
    st.markdown("## 📋 Data Detail Penjualan")
    st.dataframe(df_filter, use_container_width=True)
