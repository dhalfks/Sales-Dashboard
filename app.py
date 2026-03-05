from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="식품 수출입 대시보드", page_icon=":bar_chart:", layout="wide")

DATA_PATH = Path("data/trade_data.csv")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["거래일자"] = pd.to_datetime(df["거래일자"])
    df["월"] = df["거래일자"].dt.month
    return df


st.title("식품 회사 수출입 대시보드")
st.caption("임시 생성 데이터(총 100건, 수입 60 / 수출 40) 기반 분석")

if not DATA_PATH.exists():
    st.error("데이터 파일이 없습니다. 먼저 `python generate_data.py`를 실행하세요.")
    st.stop()

df = load_data(DATA_PATH)

col1, col2, col3, col4 = st.columns(4)
with col1:
    selected_type = st.multiselect(
        "거래구분",
        options=sorted(df["거래구분"].unique()),
        default=sorted(df["거래구분"].unique()),
    )
with col2:
    month_options = ["전체"] + list(range(1, 13))
    selected_month = st.selectbox("월 선택", options=month_options, index=0)
with col3:
    country_options = ["전체"] + sorted(df["국가"].unique().tolist())
    selected_country = st.selectbox("국가 선택", options=country_options, index=0)
with col4:
    item_options = ["전체"] + sorted(df["품목"].unique().tolist())
    selected_item = st.selectbox("품목 선택", options=item_options, index=0)

filtered = df[df["거래구분"].isin(selected_type)].copy()
if selected_month != "전체":
    filtered = filtered[filtered["월"] == selected_month]
if selected_country != "전체":
    filtered = filtered[filtered["국가"] == selected_country]
if selected_item != "전체":
    filtered = filtered[filtered["품목"] == selected_item]

if filtered.empty:
    st.warning("선택한 조건에 맞는 데이터가 없습니다.")
    st.stop()

total_amount = int(filtered["금액"].sum())
total_qty = int(filtered["수량"].sum())
import_amount = int(filtered.loc[filtered["거래구분"] == "수입", "금액"].sum())
export_amount = int(filtered.loc[filtered["거래구분"] == "수출", "금액"].sum())

m1, m2, m3, m4 = st.columns(4)
m1.metric("총 거래 금액", f"{total_amount:,} 원")
m2.metric("총 거래 수량", f"{total_qty:,}")
m3.metric("수입 금액", f"{import_amount:,} 원")
m4.metric("수출 금액", f"{export_amount:,} 원")

pie_data = filtered.groupby("거래구분", as_index=False)["금액"].sum()
fig_pie = px.pie(
    pie_data,
    names="거래구분",
    values="금액",
    title="수입 vs 수출 비중(금액)",
    hole=0.35,
)

monthly_amount = (
    filtered.groupby(["월", "거래구분"], as_index=False)["금액"]
    .sum()
    .sort_values(["월", "거래구분"])
)
fig_monthly = px.bar(
    monthly_amount,
    x="월",
    y="금액",
    color="거래구분",
    barmode="group",
    title="월별 수출입 금액",
    labels={"월": "월", "금액": "금액(원)", "거래구분": "거래구분"},
)

top_left, top_right = st.columns(2)
with top_left:
    st.plotly_chart(fig_pie, use_container_width=True)
with top_right:
    st.plotly_chart(fig_monthly, use_container_width=True)

st.subheader("국가별 수출입 내역")
if selected_country == "전체":
    country_amount = (
        filtered.groupby(["국가", "거래구분"], as_index=False)["금액"].sum().sort_values("금액", ascending=False)
    )
    fig_country = px.bar(
        country_amount,
        x="국가",
        y="금액",
        color="거래구분",
        barmode="group",
        title="국가별 수출입 금액",
        labels={"국가": "국가", "금액": "금액(원)", "거래구분": "거래구분"},
    )
else:
    country_monthly = (
        filtered.groupby(["월", "거래구분"], as_index=False)["금액"]
        .sum()
        .sort_values(["월", "거래구분"])
    )
    fig_country = px.line(
        country_monthly,
        x="월",
        y="금액",
        color="거래구분",
        markers=True,
        title=f"{selected_country} 월별 수출입 금액",
        labels={"월": "월", "금액": "금액(원)", "거래구분": "거래구분"},
    )
st.plotly_chart(fig_country, use_container_width=True)

st.subheader("품목별 수출입 내역")
item_amount = (
    filtered.groupby(["품목", "거래구분"], as_index=False)["금액"]
    .sum()
    .sort_values("금액", ascending=False)
    .head(15)
)
fig_item = px.bar(
    item_amount,
    x="금액",
    y="품목",
    color="거래구분",
    orientation="h",
    barmode="group",
    title="품목별 수출입 금액 TOP 15",
    labels={"금액": "금액(원)", "품목": "품목", "거래구분": "거래구분"},
)
st.plotly_chart(fig_item, use_container_width=True)

st.subheader("필터링된 원본 데이터")
st.dataframe(filtered.sort_values("거래일자"), use_container_width=True, hide_index=True)
