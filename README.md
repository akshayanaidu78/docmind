# 📄 DocMind

**DocMind** is a document question-answering system that allows users to upload a PDF and ask questions about its content.

Instead of manually searching through a large document, users can ask questions in natural language. DocMind retrieves the most relevant sections of the document, extracts an answer, and displays the source page for verification.

> **Current version:** Retrieval-based document QA using TF-IDF.
> **Future upgrade:** Embedding-based retrieval and LLM-powered answer generation.

---

## 🎯 Problem Statement

Large PDF documents such as academic notes, policies, guidelines, and technical documents can contain a lot of information.

Finding a specific answer manually requires repeatedly searching through pages and reading surrounding content.

DocMind aims to make this process faster by allowing users to **ask questions directly about a document**.

---

## 💡 Solution

DocMind converts the content of an uploaded PDF into searchable text.

When a user asks a question:

1. The PDF text is extracted.
2. The document is divided into smaller chunks.
3. The question is converted into a TF-IDF vector.
4. Document chunks are also represented using TF-IDF.
5. Cosine similarity is used to find the most relevant chunks.
6. Relevant content is used to extract an answer.
7. The source page is displayed along with the answer.

---

## ✨ Features

* 📤 Upload PDF documents
* 📖 Extract text from PDFs
* ✂️ Divide documents into searchable chunks
* 🔎 Retrieve relevant document content
* 💡 Generate an answer from retrieved content
* 📑 Display the source page
* ⚡ Works without an external LLM API
* 🌐 Simple web interface using Streamlit

---

## 🏗️ How It Works

```text
              PDF Upload
                   │
                   ▼
          Text Extraction
             (PyMuPDF)
                   │
                   ▼
              Chunking
                   │
                   ▼
          TF-IDF Vectorization
                   │
                   ▼
          Cosine Similarity
                   │
                   ▼
        Relevant Chunks Retrieved
                   │
                   ▼
          Answer Extraction
                   │
                   ▼
          Answer + Source Page
```

---

## 🛠️ Tech Stack

| Technology   | Purpose                      |
|--------------|------------------------------|
| Python       | Core application logic       |
| Streamlit    | Web application interface    |
| PyMuPDF      | PDF text extraction          |
| scikit-learn | TF-IDF and cosine similarity |
| Git          | Version control              |
| GitHub       | Source-code hosting          |

---

## 📂 Project Structure

```text
docmind/
│
├── app.py
├── answer_generator.py
├── chunk_text.py
├── retriever.py
├── requirements.txt
├── README.md
│
└── documents/
    └── sample.pdf
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd docmind
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Example

### Input

Upload a Software Engineering PDF and ask:

```text
What are the phases of SDLC?
```

### Output

DocMind retrieves the relevant section and displays the phases along with the source page.

```text
1. Phase 1: Requirement collection and analysis
2. Phase 2: Feasibility study
3. Phase 3: Design
4. Phase 4: Coding
5. Phase 5: Testing
6. Phase 6: Installation/Deployment
7. Phase 7: Maintenance
```

**Source:** Page 14

---

## 🔍 Retrieval Approach

DocMind currently uses **TF-IDF (Term Frequency–Inverse Document Frequency)** for information retrieval.

Each document chunk is converted into a numerical vector. The user's question is converted into another vector.

Cosine similarity is then used to measure the similarity between the question and each document chunk.

The chunks with the highest similarity scores are selected as the most relevant content.

This approach provides a simple and interpretable retrieval baseline without requiring an external AI API.

---

## ⚠️ Current Limitations

The current version has several limitations:

* TF-IDF primarily relies on matching terms rather than understanding deep semantic meaning.
* Answer generation is rule-based rather than LLM-powered.
* Complex questions may not always produce ideal answers.
* The system currently works with text extracted from PDFs and does not perform advanced multimodal document understanding.

These limitations are intentional for the current MVP.

---

## 🚀 Future Improvements

Planned improvements include:

* Replace TF-IDF with embedding-based semantic retrieval.
* Add a vector database for scalable document search.
* Integrate an LLM for natural-language answer generation.
* Improve citation accuracy and source highlighting.
* Support larger document collections.
* Add conversation history.
* Improve handling of tables and structured PDF content.

---

## 📌 Project Status

**Current Status: MVP Complete**

The current implementation supports the complete basic document question-answering pipeline:

```text
Upload → Extract → Chunk → Retrieve → Answer → Source
```

The LLM integration is planned as a future enhancement rather than a requirement for the current MVP.

---

## 👨‍💻 Author

**Akshaya Naidu**

Built as a practical project to explore document processing, information retrieval, and AI-assisted question answering.
