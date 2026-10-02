"""Questionnaire field definitions shared by validation and the final summary."""

LIKERT_OPTIONS = (
    "Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree",
)
QUESTION_PAIRS = tuple((page, page + 1) for page in range(10, 22, 2))
SUMMARY_PAGE = 22
DEMOGRAPHICS_PAGE = "demographics"
UNDERSTANDING_CHECK_PAGE = "understanding_check"
# Stable page IDs keep existing questionnaire/database field names unchanged.
PAGE_ORDER = (1, DEMOGRAPHICS_PAGE, *range(2, 8), UNDERSTANDING_CHECK_PAGE, *range(8, 23))
VALIDATION_MESSAGE = "Please answer all the fields before proceeding"

DEMOGRAPHIC_LABELS = {
    "age_group": "Age",
    "region": "Region of residence",
    "diploma": "Highest achieved or ongoing diploma",
}
DEMOGRAPHIC_OPTIONS = {
    "age_group": ("<18", "18-25", "25-40", "+40"),
    "region": ("Europe", "North America", "South America", "Australia", "Asia", "Other"),
    "diploma": ("secondary education", "college", "master degree", "phd"),
}

UNDERSTANDING_CHECK_PROMPT = (
    "Why couldn’t Julie be matched with Ana, considering rank-envy-freeness?"
)
UNDERSTANDING_CHECK_OPTIONS = {
    1: "Because Luc would envy Julie as he has only his second preferred choice.",
    2: "Because Ana would get her last choice.",
    3: "Because Ana would rank-envy Paul.",
}


def answer_page_key(page):
    return f"page{page}" if isinstance(page, int) else page

COMMON_RATING_LABELS = {
    "algorithm_working": "From the explanation, I understand why the proposed assignment can be considered fair.",
    "satisfaction": "The explanation is satisfactory.",
    "detail": "The explanation has sufficient detail.",
    "completeness": "The explanation contains irrelevant details.",
}


def question_fields(page):
    if page == DEMOGRAPHICS_PAGE:
        return DEMOGRAPHIC_LABELS
    if page == UNDERSTANDING_CHECK_PAGE:
        return {"answer": UNDERSTANDING_CHECK_PROMPT}
    if page not in range(10, 22):
        return {}
    topic = "why there is no fair matching."
    if page in (14, 15):
        topic = "why Luc cannot have a preferred roommate."
    elif page in (20, 21):
        topic = "why Paul cannot have a preferred roommate."
    if page % 2 == 0:
        return {"understanding": f"It is clear to me {topic}"}
    return {
        "understanding": f"Now, I understand {topic}",
        **COMMON_RATING_LABELS,
        "feedback": "What did you think of the algorithm’s explanations?",
    }


def page_is_complete(page, answers):
    """All questionnaire fields are required; drafts may be partial."""
    values = answers.get(answer_page_key(page), {})
    if page == DEMOGRAPHICS_PAGE:
        return all(values.get(field) in options
                   for field, options in DEMOGRAPHIC_OPTIONS.items())
    if page == UNDERSTANDING_CHECK_PAGE:
        # Check only that one option was chosen. Never grade the choice.
        value = values.get("answer")
        return type(value) is int and value in UNDERSTANDING_CHECK_OPTIONS
    for field in question_fields(page):
        value = values.get(field)
        if field == "feedback":
            if not isinstance(value, str) or not value.strip():
                return False
        elif value not in LIKERT_OPTIONS:
            return False
    return True


def first_incomplete_page(answers):
    return next((page for page in (DEMOGRAPHICS_PAGE, UNDERSTANDING_CHECK_PAGE, *range(10, 22))
                 if not page_is_complete(page, answers)), None)
