"""Convert saved questionnaire answers into one flat database row."""

from .schema import (
    DEMOGRAPHICS_PAGE,
    DEMOGRAPHIC_OPTIONS,
    LIKERT_OPTIONS,
    QUESTION_PAIRS,
    UNDERSTANDING_CHECK_PAGE,
    first_incomplete_page,
)


def build_evaluation_row(answers, *, column_names=None):
    """Return database column names mapped to encoded participant answers.

    Pass st.session_state["evaluation_answers"] or payload["answers"].
    All questionnaire answers must be complete; otherwise ValueError is raised.
    The original answers are not modified, and nothing is sent to a database.

    Demographics use zero-based indexes from DEMOGRAPHIC_OPTIONS. Their default
    output columns are age_group, region, and diploma, matching the app's keys.
    Likert ratings use zero-based indexes from LIKERT_OPTIONS (0 through 4).
    Feedback text is preserved exactly, including spaces and newlines.
    understanding_check_answer retains its existing option code (1, 2, or 3).

    For each scenario i, output columns are qi followed by pre, post,
    understand, sat, detail, irrelevant, and text; for example q1pre.
    The existing field "completeness" now means irrelevant details and maps
    to qiirrelevant. Its rating is stored as selected, without reverse scoring.

    Use column_names to override output names if your database differs:
        build_evaluation_row(answers, column_names={"age_group": "age"})
    Unspecified columns keep their default names. Metadata such as session_id
    and complete is not included because it is not participant input.
    """
    missing_page = first_incomplete_page(answers)
    if missing_page is not None:
        raise ValueError(
            f"Cannot build a database row: missing or invalid answers on page {missing_page}."
        )

    demographics = answers[DEMOGRAPHICS_PAGE]
    row = {
        field: options.index(demographics[field])
        for field, options in DEMOGRAPHIC_OPTIONS.items()
    }
    row["understanding_check_answer"] = answers[UNDERSTANDING_CHECK_PAGE]["answer"]

    post_fields = {
        "post": "understanding",
        "understand": "algorithm_working",
        "sat": "satisfaction",
        "detail": "detail",
        "irrelevant": "completeness",
    }
    for number, (before_page, after_page) in enumerate(QUESTION_PAIRS, start=1):
        before = answers[f"page{before_page}"]
        after = answers[f"page{after_page}"]
        row[f"q{number}pre"] = LIKERT_OPTIONS.index(before["understanding"])
        for suffix, field in post_fields.items():
            row[f"q{number}{suffix}"] = LIKERT_OPTIONS.index(after[field])
        row[f"q{number}text"] = after["feedback"]

    if column_names is not None:
        unknown = set(column_names) - set(row)
        if unknown:
            raise ValueError(f"Unknown output columns in column_names: {sorted(unknown)}")
        names = [column_names.get(key, key) for key in row]
        if any(not isinstance(name, str) or not name.strip() for name in names):
            raise ValueError("Database column names must be nonempty strings.")
        if len(set(names)) != len(names):
            raise ValueError("column_names must not map two answers to the same column.")
        row = dict(zip(names, row.values()))

    return row
