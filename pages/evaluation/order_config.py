"""Your six Williams sequences and the existing Supabase connection settings."""

import streamlit as st

ORDERS = (
    (1, 2, 6, 3, 5, 4),
    (2, 3, 1, 4, 6, 5),
    (3, 4, 2, 5, 1, 6),
    (4, 5, 3, 6, 2, 1),
    (5, 6, 4, 1, 3, 2),
    (6, 1, 5, 2, 4, 3),
)

def get_supabase_client():
    """Create a client only when this session first launches the questionnaire.

    Uses the same secret names as the database example in your uploaded app.
    Keep credentials in Streamlit secrets, never in these Python files.
    """
    key = "_evaluation_supabase_client"
    if key not in st.session_state:
        from supabase import create_client

        st.session_state[key] = create_client(
            st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"],
        )
    return st.session_state[key]
