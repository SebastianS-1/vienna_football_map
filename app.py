import streamlit as st
from src.data_processing import load_matches, get_upcoming_matches

st.title("Vienna Football Map")

st.write("Welcome to the Vienna Football Map!")

st.header("Upcoming Football Matches")

matches = load_matches()
upcoming_matches = get_upcoming_matches(matches)
st.dataframe(
    upcoming_matches,
    column_config={
        "date": st.column_config.DateColumn(
            "Date",
            format="DD.MM.YYYY"
        )
    }
)