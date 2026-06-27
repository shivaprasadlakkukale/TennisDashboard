import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

st.title("🌍 Country Analysis")

conn = get_connection()

# --------------------------------
# Competitors per Country
# --------------------------------

st.subheader("🏆 Competitors by Country")

country_query = """
SELECT
    country,
    COUNT(*) AS total_competitors
FROM competitor
GROUP BY country
ORDER BY total_competitors DESC
"""

country_df = pd.read_sql(country_query, conn)

st.dataframe(country_df, use_container_width=True)

fig1 = px.bar(
    country_df,
    x="country",
    y="total_competitors",
    title="Competitors per Country"
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------
# Average Points by Country
# --------------------------------

st.subheader("📈 Average Points by Country")

avg_points_query = """
SELECT
    c.country,
    ROUND(AVG(r.points),2) AS avg_points
FROM competitor c
JOIN rankings r
ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY avg_points DESC
"""

avg_df = pd.read_sql(avg_points_query, conn)

st.dataframe(avg_df, use_container_width=True)

fig2 = px.bar(
    avg_df,
    x="country",
    y="avg_points",
    title="Average Points by Country"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------
# Country Filter
# --------------------------------

st.subheader("🔍 Country Details")

countries = sorted(country_df["country"].dropna().unique())

selected_country = st.selectbox(
    "Select Country",
    countries
)

country_details_query = f"""
SELECT
    c.competitor_name,
    r.rank,
    r.points,
    r.movement,
    r.competitions_played
FROM competitor c
JOIN rankings r
ON c.competitor_id = r.competitor_id
WHERE c.country = '{selected_country}'
ORDER BY r.rank
"""

details_df = pd.read_sql(country_details_query, conn)

st.dataframe(details_df, use_container_width=True)

conn.close()