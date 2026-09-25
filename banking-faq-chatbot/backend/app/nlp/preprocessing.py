import spacy
from backend.app.config import SPACY_MODEL

_nlp = spacy.load(SPACY_MODEL, disable=["ner", "parser"])


def clean_text(text: str) -> str:

    if not text or not text.strip():
        return ""

    doc = _nlp(text.lower())

    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
        and token.lemma_.strip()
    ]

    return " ".join(tokens)

def build_matching_text(question: str, alternates: list[str], keywords: list[str]) -> str:

    combined = " ".join([question, *alternates, *keywords])
    return clean_text(combined)