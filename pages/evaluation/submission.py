"""Database integration point called only after a valid Finish action."""

from .database import get_supabase_client
from .database_row import build_evaluation_row


def save_evaluation(payload):
    """Encode participant answers and insert one row into evaluation.

    Conversion and database errors propagate to the Finish handler, which
    keeps the questionnaire open for retry. Only the client is cached; each
    call performs an insert. The insert requests no row data in its response,
    so an INSERT policy is sufficient.
    """
    answers_dict = build_evaluation_row(payload["answers"])
    print("The given answres dict is ")
    print(answers_dict)
    supabase = get_supabase_client()
    supabase.table("evaluation").insert(
        answers_dict, returning="minimal",
    ).execute()
