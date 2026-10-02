import streamlit as st

from pages.evaluation import questions
from pages.evaluation.state import (
    PRELIMINARY_PAGES, begin_page, finish_evaluation, initialize_evaluation, navigate,
)
from pages.evaluation.summary import render_summary
from pages.evaluation.ordering import get_page_order
from pages.evaluation.schema import (
    DEMOGRAPHICS_PAGE, SUMMARY_PAGE, UNDERSTANDING_CHECK_PAGE,
)

st.set_page_config(layout="wide")

PAGES = {
    int(name[4:]): render
    for name, render in vars(questions).items()
    if name.startswith("page") and name[4:].isdigit() and callable(render)
}
PAGES[UNDERSTANDING_CHECK_PAGE] = questions.understanding_check
PAGES[DEMOGRAPHICS_PAGE] = questions.demographics

st.markdown("""
    <style>
        .block-container {
            max-width: 70rem;
            padding-left: 2rem;
            padding-right: 2rem;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

initialize_evaluation()
begin_page()
st.session_state["agents"] = list(range(6))
page = st.session_state["epi"]
complete = st.session_state["evaluation_complete"]
phase = "complete" if complete else "answer"
page_order = get_page_order()

if not complete:
    st.caption(f"Page {page_order.index(page) + 1} of {len(page_order)}")
    if page in range(10, SUMMARY_PAGE) or page in (DEMOGRAPHICS_PAGE, UNDERSTANDING_CHECK_PAGE):
        st.caption("Your answers are saved when you select Previous or Next.")
        st.caption("All fields are required to continue.")


def render_navigation(*, in_form):
    button = st.form_submit_button if in_form else st.button
    fields = dict(st.session_state["_evaluation_fields"])
    if st.session_state["evaluation_error"]:
        st.error(st.session_state["evaluation_error"])
    cols = st.columns([1, 4, 1])
    with cols[0]:
        button(
            "Previous", disabled=page == 1 and not complete,
            on_click=navigate, args=(-1, page, fields),
        )
    with cols[2]:
        if page == SUMMARY_PAGE:
            button("Finish", type="primary", on_click=finish_evaluation)
        else:
            button(
                "Next", type="primary",
                on_click=navigate, args=(1, page, fields),
            )


if complete:
    st.title("Evaluation complete")
    st.success("Thank you! Your evaluation is complete.")
    submission = st.session_state["evaluation_submission"]
    render_summary(submission["answers"], submission.get("question_order"))
    st.success("Thank you! Your evaluation is complete.")
elif page in PRELIMINARY_PAGES:
    # Original Yes/No buttons show feedback immediately. Their one-run values
    # reset on navigation, so returning to a preliminary question starts fresh.
    # Regular buttons must be outside a form.
    PAGES[page]()
    render_navigation(in_form=False)
else:
    # Ratings, feedback, and navigation share a form; Check remains a popover.
    # Enter in a text box must not accidentally activate Previous.
    with st.form(f"evaluation_page_{page}_{phase}", clear_on_submit=False,
                 enter_to_submit=False, border=False):
        PAGES[page]()
        render_navigation(in_form=True)
