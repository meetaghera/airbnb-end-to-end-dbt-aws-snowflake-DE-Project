import streamlit as st
import snowflake.connector
import pandas as pd

@st.cache_resource
def get_connection():
    conn = snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"],
    )
    return conn

@st.cache_data(ttl=3600)
def run_query(query: str) -> pd.DataFrame:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        df = cur.fetch_pandas_all()
    finally:
        cur.close()
    return df
