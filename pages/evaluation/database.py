"""Cached Supabase client for the questionnaire's database operations."""

import streamlit as st


@st.cache_resource(show_spinner=False)
def get_supabase_client():
    """Reuse the app's database client across sessions and script reruns.

    This client uses the app's shared credentials. Do not sign participants
    in or change its authentication state; participant data stays in Session
    State. Cache the client, not RPC results or database writes.
    """
    from supabase import create_client

    return create_client(
        st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"],
    )
