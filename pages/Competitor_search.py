import streamlit as st
import pandas as pd
from db import get_connection

st.title("🔍 Competitor Search")

conn = get_connection()

search = st.text_input("Enter Competitor Name")

query = f"""
SELECT c.competitor_name,
       c.country,
       r.rank,
       r.points,
       r.movement,
       r.competitions_played
FROM competitor c
JOIN rankings r
ON c.competitor_id = r.competitor_id
WHERE c.competitor_name LIKE '%{search}%'
"""

df = pd.read_sql(query, conn)

st.dataframe(df)

conn.close()