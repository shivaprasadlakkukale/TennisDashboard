import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Tennis Analytics Dashboard",
    page_icon="🎾",
    layout="wide"
)

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------
conn = get_connection()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🎾 Tennis Dashboard")
st.sidebar.markdown("Use the navigation menu below.")

# Country Filter
countries = pd.read_sql(
    "SELECT DISTINCT country FROM competitor ORDER BY country",
    conn
)

country_options = ["All"] + countries["country"].dropna().tolist()

selected_country = st.sidebar.selectbox(
    "🌍 Select Country",
    country_options
)

# Rank Filter
rank_limit = st.sidebar.slider(
    "🏆 Maximum Rank",
    min_value=1,
    max_value=5000,
    value=100
)

# Competitor Search
search_name = st.sidebar.text_input(
    "🔍 Search Competitor"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🎾 Tennis Rankings Explorer")
st.markdown(
    "### Interactive Dashboard for Tennis Rankings, Competitors and Competitions"
)

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

total_competitors = pd.read_sql(
    "SELECT COUNT(*) AS total FROM competitor",
    conn
).iloc[0]["total"]

total_countries = pd.read_sql(
    "SELECT COUNT(DISTINCT country) AS total FROM competitor",
    conn
).iloc[0]["total"]

highest_points = pd.read_sql(
    "SELECT MAX(points) AS max_points FROM rankings",
    conn
).iloc[0]["max_points"]

total_competitions = pd.read_sql(
    "SELECT COUNT(*) AS total FROM competitions",
    conn
).iloc[0]["total"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👤 Competitors", total_competitors)

with col2:
    st.metric("🌍 Countries", total_countries)

with col3:
    st.metric("🏆 Highest Points", highest_points)

with col4:
    st.metric("🎾 Competitions", total_competitions)

st.divider()

# ---------------------------------------------------
# FILTERED RANKINGS
# ---------------------------------------------------

query = """
SELECT
c.competitor_name,
c.country,
r.rank,
r.points,
r.movement,
r.competitions_played
FROM rankings r
JOIN competitor c
ON r.competitor_id = c.competitor_id
WHERE r.rank <= %s
"""

params = [rank_limit]

if selected_country != "All":
    query += " AND c.country = %s"
    params.append(selected_country)

if search_name:
    query += " AND c.competitor_name LIKE %s"
    params.append(f"%{search_name}%")

query += " ORDER BY r.rank ASC"

ranking_df = pd.read_sql(
    query,
    conn,
    params=params
)

st.subheader("🏆 Filtered Rankings")

st.dataframe(
    ranking_df,
    use_container_width=True,
    height=400
)

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

col1, col2 = st.columns(2)

# Country Chart
with col1:

    country_df = pd.read_sql("""
        SELECT
            country,
            COUNT(*) AS total_players
        FROM competitor
        GROUP BY country
        ORDER BY total_players DESC
        LIMIT 10
    """, conn)

    fig_country = px.bar(
        country_df,
        x="country",
        y="total_players",
        title="Top 10 Countries by Competitors"
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )

# Points Chart
with col2:

    points_df = pd.read_sql("""
        SELECT
            c.competitor_name,
            r.points
        FROM rankings r
        JOIN competitor c
        ON r.competitor_id = c.competitor_id
        ORDER BY r.points DESC
        LIMIT 10
    """, conn)

    fig_points = px.bar(
        points_df,
        x="competitor_name",
        y="points",
        title="Top 10 Players by Points"
    )

    st.plotly_chart(
        fig_points,
        use_container_width=True
    )

st.divider()

# ---------------------------------------------------
# TOP PLAYERS TABLE
# ---------------------------------------------------

st.subheader("🥇 Top Ranked Competitors")

top_players = pd.read_sql("""
SELECT
    c.competitor_name,
    c.country,
    r.rank,
    r.points,
    r.movement,
    r.competitions_played
FROM rankings r
JOIN competitor c
ON r.competitor_id = c.competitor_id
ORDER BY r.rank ASC
LIMIT 20
""", conn)

st.dataframe(
    top_players,
    use_container_width=True
)

st.divider()

# ---------------------------------------------------
# COMPETITION ANALYSIS
# ---------------------------------------------------

st.subheader("🎾 Competition Distribution")

competition_df = pd.read_sql("""
SELECT
    type,
    COUNT(*) AS total
FROM competitions
GROUP BY type
""", conn)

fig_comp = px.pie(
    competition_df,
    names="type",
    values="total",
    title="Competition Type Distribution"
)

st.plotly_chart(
    fig_comp,
    use_container_width=True
)

st.divider()

# ---------------------------------------------------
# QUICK INSIGHTS
# ---------------------------------------------------

st.subheader("📈 Quick Insights")

col1, col2 = st.columns(2)

world_no1 = pd.read_sql("""
SELECT
    c.competitor_name,
    r.rank
FROM rankings r
JOIN competitor c
ON r.competitor_id = c.competitor_id
ORDER BY r.rank ASC
LIMIT 1
""", conn)

highest_player = pd.read_sql("""
SELECT
    c.competitor_name,
    r.points
FROM rankings r
JOIN competitor c
ON r.competitor_id = c.competitor_id
ORDER BY r.points DESC
LIMIT 1
""", conn)

with col1:
    st.success(
        f"🏆 Current World No.1: {world_no1.iloc[0]['competitor_name']}"
    )

with col2:
    st.info(
        f"⭐ Highest Points Holder: {highest_player.iloc[0]['competitor_name']} ({highest_player.iloc[0]['points']} points)"
    )

st.divider()

st.caption(
    "🎾 Tennis Analytics Dashboard "
)

conn.close()