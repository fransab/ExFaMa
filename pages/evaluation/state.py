"""Session-only questionnaire answers, independent of widget lifetimes."""

from copy import deepcopy
from uuid import uuid4

import streamlit as st

from .schema import (
    SUMMARY_PAGE, VALIDATION_MESSAGE, answer_page_key, page_is_complete,
)
from .submission import save_evaluation
from .ordering import get_page_order, get_question_order, set_question_order
from .order_assignment import ensure_question_order

import traceback

PRELIMINARY_PAGES = frozenset(range(3, 8))


def initialize_evaluation(question_order=None):
    if question_order is not None:
        set_question_order(question_order)
    st.session_state.setdefault("epi", 1)
    st.session_state.setdefault("evaluation_session_id", str(uuid4()))
    st.session_state.setdefault("evaluation_answers", {})
    st.session_state.setdefault("evaluation_complete", False)
    st.session_state.setdefault("evaluation_error", None)
    # A completion screen from the previous version is now the review screen.
    if st.session_state["evaluation_complete"] and "evaluation_submission" not in st.session_state:
        st.session_state["evaluation_complete"] = False
        st.session_state["epi"] = SUMMARY_PAGE
    # Preliminary answers are intentionally temporary. Discard state retained
    # by the earlier radio/review implementation if an active session has it.
    st.session_state.pop("evaluation_review", None)
    for page in PRELIMINARY_PAGES:
        st.session_state["evaluation_answers"].pop(f"page{page}", None)


def begin_page():
    # Only fields actually rendered on this screen are submitted by its form.
    st.session_state["_evaluation_fields"] = {}


def answer_key(page, field, default=None):
    """Register a field and restore its last submitted value before rendering."""
    widget_key = f"_evaluation:{page}:{field}"
    saved = st.session_state["evaluation_answers"].get(page, {})
    if widget_key not in st.session_state:
        st.session_state[widget_key] = saved.get(field, default)
    st.session_state["_evaluation_fields"][field] = widget_key
    return widget_key


def navigate(direction, page, fields):
    """Save the newly submitted batch before changing the visible screen.

    Read widget values here, rather than passing their old values as callback
    arguments. Streamlit updates form state before running this callback.
    """
    if st.session_state["evaluation_complete"]:
        return
    st.session_state["evaluation_error"] = None
    if fields:
        answers = st.session_state["evaluation_answers"]
        answers.setdefault(answer_page_key(page), {}).update(
            {field: st.session_state[key] for field, key in fields.items()}
        )

    # Validate the submitted batch, not the values from the preceding render.
    # Previous always saves drafts without enforcing completeness.
    if direction == 1 and not page_is_complete(page, st.session_state["evaluation_answers"]):
        st.session_state["evaluation_error"] = VALIDATION_MESSAGE
        return

    if direction == 1 and page == 9:
        try:
            ensure_question_order()
        except Exception:
            st.session_state["evaluation_error"] = (
                "Could not assign a question order. Please try again."
            )
            return

    page_order = get_page_order()
    position = page_order.index(page)
    next_position = max(0, min(len(page_order) - 1, position + direction))
    st.session_state["epi"] = page_order[next_position]


def finish_evaluation():
    """Recheck the full questionnaire, then prepare one final submission."""
    if st.session_state["evaluation_complete"]:
        return
    st.session_state["evaluation_error"] = None
    missing_page = next(
        (page for page in get_page_order()
         if not page_is_complete(page, st.session_state["evaluation_answers"])),
        None,
    )
    if missing_page is not None:
        st.session_state["epi"] = missing_page
        st.session_state["evaluation_error"] = VALIDATION_MESSAGE
        return

    payload = evaluation_payload()
    payload["complete"] = True
    try:
        save_evaluation(deepcopy(payload))
    except Exception:
        # Do not mark the session finished if a future database write fails.
        st.session_state["evaluation_error"] = (
            "We couldn't finish the evaluation. Please try again."
        )
        print("Tried to send payload ")
        print(payload["answers"])
        print("---")
        traceback.print_exc()
        return
    st.session_state["evaluation_submission"] = payload
    st.session_state["evaluation_complete"] = True


def evaluation_payload():
    """Return a JSON-serializable snapshot for a future database integration.

    This function does not write to a database or share data between sessions.
    Use session_id as an upsert key when adding persistent storage.
    """
    payload = {
        "session_id": st.session_state["evaluation_session_id"],
        "answers": st.session_state["evaluation_answers"],
        "complete": st.session_state["evaluation_complete"],
        "question_order": list(get_question_order()),
    }
    assignment = st.session_state.get("evaluation_database_assignment")
    if assignment is not None:
        payload["assigned_order"] = assignment["assigned_order"]
        payload["order_index"] = assignment["order_index"]
    return deepcopy(payload)
