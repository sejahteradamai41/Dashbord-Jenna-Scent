import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
print("Hello Learners")
# reading the data from excel file
df = pd.read_excel("penjualan -jenna.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('Jenna-logo.jpeg')

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Penjualan Jenna Scent</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

with col4:

    # === GRAFIK YANG VALID BERDASARKAN KOLOM DATA YANG ADA ===
    fig = px.bar(
        df,
        x="Varian",             # kolom yang tersedia
        y="Quantity",           # kolom yang tersedia
        labels={"Quantity": "Jumlah Terjual"},
        title="Total Quantity per Varian",
        template="gridon",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # === TABEL DETAIL BARANG ===
    st.subheader("📌 Detail Data Barang")

    data_barang = df[[
        "No",
        "Tanggal",
        "Varian",
        "Quantity",
        "Harga Barang",
        "HPP",
        "Stok Barang"
    ]].copy()

    st.dataframe(data_barang, use_container_width=True)
with col5:
    st.subheader("Analisis Varian & Harga Parfum")

    # ================================
    # 1️⃣ PIE CHART — Varian Paling Laris
    # ================================
    varian_laris = df.groupby("Varian")["Quantity"].sum().reset_index()

    fig_pie = px.pie(
        varian_laris,
        names="Varian",
        values="Quantity",
        title="Varian Parfum Paling Laris",
        hole=0.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)
