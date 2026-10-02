"""Read-only review of all questionnaire answers, grouped by study question."""

import streamlit as st

from .schema import (
    DEMOGRAPHICS_PAGE, DEMOGRAPHIC_LABELS,
    UNDERSTANDING_CHECK_PAGE, UNDERSTANDING_CHECK_PROMPT,
    UNDERSTANDING_CHECK_OPTIONS, question_fields,
)
from .ordering import get_question_pairs


def render_summary(answers, question_order=None):
    st.subheader("About you")
    demographics = answers.get(DEMOGRAPHICS_PAGE, {})
    st.table([
        {"Question": label, "Answer": demographics.get(field) or "Not answered"}
        for field, label in DEMOGRAPHIC_LABELS.items()
    ])
    st.subheader("Understanding check")
    st.write(UNDERSTANDING_CHECK_PROMPT)
    choice = answers.get(UNDERSTANDING_CHECK_PAGE, {}).get("answer")
    st.text(UNDERSTANDING_CHECK_OPTIONS.get(choice, "Not answered"))
    for number, (before_page, after_page) in enumerate(get_question_pairs(question_order), start=1):
        st.subheader(f"Question {number}")
        rows = []
        for page, stage in ((before_page, "Before explanation"),
                            (after_page, "After explanation")):
            saved = answers.get(f"page{page}", {})
            for field, label in question_fields(page).items():
                if field != "feedback":
                    rows.append({"Stage": stage, "Question": label,
                                 "Answer": saved.get(field) or "Not answered"})
        st.table(rows)
        st.markdown("**Your feedback**")
        feedback = answers.get(f"page{after_page}", {}).get("feedback") or ""
        # Participant text is displayed literally, preserving newlines.
        st.text(feedback if feedback.strip() else "Not answered")
