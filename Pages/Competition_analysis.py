import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

st.title("🎾 Competition Analysis")

conn = get_connection()

# Load competition data
df = pd.read_sql("SELECT * FROM competitions", conn)

# ----------------------------
# Competition Data
# ----------------------------
st.subheader("📋 Competition Data")
st.dataframe(df, use_container_width=True)

# ----------------------------
# Filters
# ----------------------------
st.subheader("🔍 Filters")

col1, col2, col3 = st.columns(3)

with col1:
    selected_type = st.selectbox(
        "Competition Type",
        ["All"] + sorted(df["type"].dropna().unique().tolist())
    )

with col2:
    selected_gender = st.selectbox(
        "Gender",
        ["All"] + sorted(df["gender"].dropna().unique().tolist())
    )

with col3:
    selected_category = st.selectbox(
        "Category ID",
        ["All"] + sorted(df["category_id"].dropna().astype(str).unique().tolist())
    )

filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category_id"].astype(str) == selected_category
    ]

st.subheader("🎯 Filtered Competitions")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------------
# Competition Type Analysis
# ----------------------------
st.subheader("📊 Competition Types")

type_df = pd.read_sql("""
SELECT type, COUNT(*) AS total
FROM competitions
GROUP BY type
""", conn)

fig1 = px.pie(
    type_df,
    names="type",
    values="total",
    title="Competition Type Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# Gender Analysis
# ----------------------------
st.subheader("👨‍🦱 Gender Distribution")

gender_df = pd.read_sql("""
SELECT gender, COUNT(*) AS total
FROM competitions
GROUP BY gender
""", conn)

fig2 = px.bar(
    gender_df,
    x="gender",
    y="total",
    title="Competitions by Gender"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Category Analysis
# ----------------------------
st.subheader("🏅 Category Distribution")

category_df = pd.read_sql("""
SELECT category_id, COUNT(*) AS total
FROM competitions
GROUP BY category_id
ORDER BY total DESC
""", conn)

fig3 = px.bar(
    category_df,
    x="category_id",
    y="total",
    title="Competitions by Category"
)

st.plotly_chart(fig3, use_container_width=True)

conn.close()