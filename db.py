import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["reseau.proxy.rlwy.net"],
        port=int(st.secrets[ "49113"]),
        user=st.secrets["root"],
        password=st.secrets["LEyhLpcGoxbCpyvRlbphPiCTgxFHHzDD"],
        database=st.secrets["railway"]
    )