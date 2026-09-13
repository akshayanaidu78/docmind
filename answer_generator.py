import re

from retriever import search


STOP_WORDS = {
    "what", "where", "when", "which", "who",
    "why", "how", "does", "the", "are", "is",
    "was", "were", "can", "could", "about",
    "a", "an", "of", "to", "for", "and"
}


def clean_lines(text):
    """Return useful non-empty lines from a chunk."""
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


def extract_definition(question, results):
    """Extract a definition-style answer."""

    for result in results:
        sentences = re.split(
            r"(?<=[.!?])\s+|\n",
            result["text"]
        )

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence.split()) < 7:
                continue

            lower = sentence.lower()

            # Ignore obvious headings.
            if any(
                word in lower
                for word in [
                    "table of contents",
                    "importance of",
                    "emergence of",
                    "notable changes"
                ]
            ):
                continue

            # Prefer actual definition patterns.
            if (
                "is the process of" in lower
                or "refers to" in lower
                or "defined as" in lower
                or " is a " in lower
                or " is an " in lower
                or "means" in lower
            ):
                return sentence, result["page"]

    return None, None


def extract_list_answer(question, results):
    """Extract a clean numbered/bulleted list."""

    question_lower = question.lower()

    list_keywords = [
        "phases",
        "steps",
        "types",
        "characteristics",
        "features",
        "advantages",
        "disadvantages",
        "principles",
        "stages",
        "models"
    ]

    if not any(
        keyword in question_lower
        for keyword in list_keywords
    ):
        return None, None

    for result in results:

        lines = clean_lines(result["text"])

        list_items = []

        for line in lines:

            # SDLC-style phase items:
            # Phase 1: ...
            # Phase 2: ...
            if re.match(
                r"^phase\s+\d+\s*:",
                line,
                re.IGNORECASE
            ):
                list_items.append(line)

            # Numbered / bullet lists
            elif re.match(
                r"^(?:\d+[\.\)]|[-•➢➤])\s*",
                line
            ):
                list_items.append(line)

        # We need at least two actual list items.
        if len(list_items) >= 2:

            # Remove duplicates.
            cleaned = []
            seen = set()

            for item in list_items:

                key = item.lower()

                if key not in seen:
                    seen.add(key)
                    cleaned.append(item)

            # For SDLC, stop after the seven phases.
            if "sdlc" in question_lower and "phases" in question_lower:
                cleaned = cleaned[:7]

            return "\n".join(
                f"{index}. {item}"
                for index, item in enumerate(
                    cleaned,
                    start=1
                )
            ), result["page"]

    return None, None

def extract_general_answer(question, results):
    """Extract the best explanatory passage for general questions."""

    question_words = {
        word.lower()
        for word in re.findall(
            r"\b[a-zA-Z]+\b",
            question
        )
        if word.lower() not in STOP_WORDS
    }

    candidates = []

    for result in results:

        sentences = re.split(
            r"(?<=[.!?])\s+|\n",
            result["text"]
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence.split()) < 7:
                continue

            sentence_words = {
                word.lower()
                for word in re.findall(
                    r"\b[a-zA-Z]+\b",
                    sentence
                )
            }

            overlap = len(
                question_words & sentence_words
            )

            if overlap > 0:
                candidates.append({
                    "text": sentence,
                    "page": result["page"],
                    "score": overlap
                })

    if not candidates:
        return (
            results[0]["text"].strip(),
            results[0]["page"]
        )

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    best = candidates[0]

    return best["text"], best["page"]


def generate_answer(question, retriever):
    """
    Search the document and generate a grounded answer.
    """

    results = search(
        question,
        retriever,
        top_k=5
    )

    if not results:
        return {
            "answer": "I could not find relevant information in the document.",
            "sources": []
        }

    # 1. Definition questions
    if "what is" in question.lower():
        answer, page = extract_definition(
            question,
            results
        )

        if answer:
            return {
                "answer": answer,
                "sources": [page]
            }

    # 2. List / phase / step questions
    answer, page = extract_list_answer(
        question,
        results
    )

    if answer:
        return {
            "answer": answer,
            "sources": [page]
        }

    # 3. General questions
    answer, page = extract_general_answer(
        question,
        results
    )

    return {
        "answer": answer,
        "sources": [page] if page else []
    }