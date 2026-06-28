import streamlit as st
import pandas as pd
from db import get_connection

st.title("🏆 Leaderboards")

conn = get_connection()

# -------------------------------
# Top Ranked Competitors
# -------------------------------
st.subheader("🥇 Top 10 Ranked Competitors")

top_ranked_query = """
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
LIMIT 10
"""

top_ranked = pd.read_sql(top_ranked_query, conn)

st.dataframe(
    top_ranked,
    use_container_width=True
)

# -------------------------------
# Highest Points
# -------------------------------
st.subheader("🔥 Top 10 Competitors by Points")

highest_points_query = """
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
ORDER BY r.points DESC
LIMIT 10
"""

highest_points = pd.read_sql(
    highest_points_query,
    conn
)

st.dataframe(
    highest_points,
    use_container_width=True
)

# -------------------------------
# Rank Filter
# -------------------------------
st.subheader("🎯 Filter Competitors by Rank")

rank_limit = st.slider(
    "Show competitors ranked up to",
    min_value=1,
    max_value=1000,
    value=100
)

filtered_query = f"""
SELECT
    c.competitor_name,
    c.country,
    r.rank,
    r.points,
    r.competitions_played
FROM rankings r
JOIN competitor c
    ON r.competitor_id = c.competitor_id
WHERE r.rank <= {rank_limit}
ORDER BY r.rank
"""

filtered_df = pd.read_sql(
    filtered_query,
    conn
)

st.dataframe(
    filtered_df,
    use_container_width=True
)

conn.close()