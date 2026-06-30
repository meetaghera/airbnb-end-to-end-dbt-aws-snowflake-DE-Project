import streamlit as st
import plotly.express as px
from connection import run_query
import queries

st.set_page_config(page_title="Airbnb Gold Layer Dashboard", layout="wide", initial_sidebar_state="expanded")

st.title("🏠 Airbnb Data Dashboard")
st.caption("Powered by dbt + Snowflake — Gold Layer (OBT)")

with st.spinner("Loading data from Snowflake..."):
    df_sample = run_query(queries.OBT_SAMPLE)
    df_city = run_query(queries.BOOKINGS_BY_CITY)
    df_room = run_query(queries.PRICE_BY_ROOM_TYPE)
    df_time = run_query(queries.BOOKINGS_OVER_TIME)
    df_superhost = run_query(queries.SUPERHOST_PERFORMANCE)
    df_status = run_query(queries.BOOKING_STATUS_BREAKDOWN)
    df_property = run_query(queries.PROPERTY_TYPE_DISTRIBUTION)

# KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings (sample)", f"{df_sample['BOOKING_ID'].nunique():,}")
col2.metric("Avg Price/Night", f"${df_sample['PRICE_PER_NIGHT'].mean():,.0f}")
col3.metric("Cities Covered", df_city.shape[0])
col4.metric("Superhost Listings", f"{(df_sample['IS_SUPERHOST'] == True).sum():,}")

st.divider()

# Row 1: Bookings by city + Price by room type
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Cities by Bookings")
    fig1 = px.bar(df_city, x="CITY", y="TOTAL_BOOKINGS", color="AVG_CHARGE",
                  title="Bookings by City")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Price by Room Type")
    fig2 = px.bar(df_room, x="ROOM_TYPE", y="AVG_PRICE",
                  title="Average Price per Night by Room Type")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 2: Revenue over time
st.subheader("Booking & Revenue Trends")
fig3 = px.line(df_time, x="BOOKING_MONTH", y="TOTAL_REVENUE",
               title="Monthly Revenue Trend", markers=True)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Row 3: Superhost performance + booking status
col1, col2 = st.columns(2)

with col1:
    st.subheader("Superhost vs Regular Host")
    fig4 = px.bar(df_superhost, x="IS_SUPERHOST", y="AVG_BOOKING_VALUE",
                  title="Avg Booking Value: Superhost vs Not")
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("Booking Status Breakdown")
    fig5 = px.pie(df_status, names="BOOKING_STATUS", values="COUNT",
                  title="Booking Status Distribution")
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# Row 4: Property type distribution
st.subheader("Top Property Types")
fig6 = px.bar(df_property, x="PROPERTY_TYPE", y="LISTING_COUNT",
              title="Listing Count by Property Type")
st.plotly_chart(fig6, use_container_width=True)

st.divider()

with st.expander("🔍 View Raw OBT Sample Data"):
    st.dataframe(df_sample, use_container_width=True)