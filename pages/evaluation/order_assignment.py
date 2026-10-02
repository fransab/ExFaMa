"""Claim a database sequence when the existing Next button leaves page 9."""

import streamlit as st

from . import order_config
from .database import get_supabase_client
from .ordering import set_question_order, validate_question_order


def _order_id(value):
    # Do not truncate floats or accept True/False as integer order IDs.
    if type(value) not in (int, str):
        raise ValueError("Expected an order ID from 1 to 6.")
    number = int(value)
    if number not in range(1, 7):
        raise ValueError("Expected an order ID from 1 to 6.")
    return number


def ensure_question_order():
    """Reuse this session's assignment, or claim and freeze one new sequence.

    The RPC returns a one-based ID. The Python ORDERS tuple is zero-based.
    This function is called only by the page-9 Next callback. Do not cache it
    globally: every new participant must make their own claim.
    """
    existing = st.session_state.get("evaluation_database_assignment")
    if existing is not None:
        set_question_order(existing["question_order"])
        return existing["assigned_order"]

    orders = order_config.ORDERS
    if not isinstance(orders, (tuple, list)) or len(orders) != 6:
        raise ValueError("Set ORDERS in order_config.py to your six question-order tuples.")
    sequences = tuple(validate_question_order(order) for order in orders)

    # Validate the local sequences before consuming a database assignment.
    if "assigned_order" in st.session_state:
        assigned_order = _order_id(st.session_state["assigned_order"])
    else:
        client = get_supabase_client()
        response = client.rpc("claim_display_order").execute()
        assigned_order = _order_id(response.data)
        st.session_state["assigned_order"] = assigned_order

    index = assigned_order - 1
    selected = sequences[index]
    set_question_order(selected)
    st.session_state["order_index"] = index
    st.session_state["evaluation_database_assignment"] = {
        "assigned_order": assigned_order,
        "order_index": index,
        "question_order": selected,
    }
    return assigned_order
