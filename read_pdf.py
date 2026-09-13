import fitz

pdf_path = "documents/sample.pdf"

document = fitz.open(pdf_path)

print("Number of pages:", len(document))
print("\n--- DOCUMENT TEXT ---\n")

for page_number, page in enumerate(document):
    text = page.get_text()

    print(f"\n===== PAGE {page_number + 1} =====")
    print(text)

document.close()