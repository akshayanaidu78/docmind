from chunk_text import extract_pages, create_chunks
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_retriever(pdf_path):
    """
    Read a PDF and build a searchable TF-IDF index.
    """

    pages = extract_pages(pdf_path)
    chunks = create_chunks(pages)

    texts = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer()
    chunk_vectors = vectorizer.fit_transform(texts)

    return {
        "chunks": chunks,
        "vectorizer": vectorizer,
        "chunk_vectors": chunk_vectors
    }


def search(query, retriever, top_k=3):
    """
    Search the uploaded document and return
    the most relevant chunks.
    """

    chunks = retriever["chunks"]
    vectorizer = retriever["vectorizer"]
    chunk_vectors = retriever["chunk_vectors"]

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        chunk_vectors
    )[0]

    ranked_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:

        results.append({
            "page": chunks[index]["page"],
            "text": chunks[index]["text"],
            "score": float(similarities[index])
        })

    return results