import pymupdf


def extract_pages(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text().strip()

        if text:
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages


def create_chunks(pages, chunk_size=1000):
    chunks = []

    for page in pages:
        text = page["text"]

        for start in range(0, len(text), chunk_size):
            chunk = text[start:start + chunk_size]

            if chunk.strip():
                chunks.append({
                    "page": page["page"],
                    "text": chunk
                })

    return chunks


if __name__ == "__main__":

    pdf_path = "documents/sample.pdf"

    pages = extract_pages(pdf_path)
    chunks = create_chunks(pages)

    print("Pages:", len(pages))
    print("Chunks:", len(chunks))

    print("\n--- FIRST 3 CHUNKS ---\n")

    for i, chunk in enumerate(chunks[:3]):
        print(f"===== CHUNK {i + 1} | PAGE {chunk['page']} =====")
        print(chunk["text"])
        print()