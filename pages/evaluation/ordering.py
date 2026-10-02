"""Arrange the six questionnaire page pairs using a supplied tuple."""

import streamlit as st

from .schema import PAGE_ORDER, QUESTION_PAIRS, SUMMARY_PAGE

ORIGINAL_QUESTION_ORDER = tuple(range(1, len(QUESTION_PAIRS) + 1))


def validate_question_order(sequence):
    """Accept a permutation of the six page-pair IDs, numbered 1 through 6."""
    try:
        sequence = tuple(sequence)
    except TypeError as exc:
        raise ValueError("Question order must contain each integer from 1 to 6 once.") from exc
    if (len(sequence) != len(ORIGINAL_QUESTION_ORDER)
            or any(type(question) is not int for question in sequence)
            or set(sequence) != set(ORIGINAL_QUESTION_ORDER)):
        raise ValueError("Question order must contain each integer from 1 to 6 once.")
    return sequence


def set_question_order(sequence):
    """Use this tuple for navigation and labels; preserve all saved answers.

    Pair 1 is pages 10/11, pair 2 is pages 12/13, ..., pair 6 is pages 20/21.
    Call before rendering the page. No database or assignment ID is involved.
    """
    sequence = validate_question_order(sequence)
    st.session_state["evaluation_question_order"] = sequence
    return sequence


def get_question_order():
    return st.session_state.get("evaluation_question_order", ORIGINAL_QUESTION_ORDER)


def get_question_pairs(question_order=None):
    sequence = get_question_order() if question_order is None else validate_question_order(question_order)
    return tuple(QUESTION_PAIRS[question - 1] for question in sequence)


def get_page_order():
    prefix = PAGE_ORDER[:PAGE_ORDER.index(QUESTION_PAIRS[0][0])]
    pages = tuple(page for pair in get_question_pairs() for page in pair)
    return (*prefix, *pages, SUMMARY_PAGE)


def question_position(original_question):
    """Displayed number for both pages of an original scenario."""
    return get_question_order().index(original_question) + 1
