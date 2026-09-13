import streamlit as st
import tempfile
import os

from retriever import build_retriever
from answer_generator import generate_answer


st.set_page_config(
    page_title="DocMind",
    page_icon="📄",
    layout="centered"
)


st.title("📄 DocMind")

st.subheader("Ask questions about your document")

st.write(
    "Upload a PDF and ask questions. "
    "DocMind searches the document and provides "
    "the answer with its source page."
)


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"Document uploaded: {uploaded_file.name}"
    )

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        pdf_path = temp_file.name

    try:

        # Build search index from THIS uploaded PDF
        with st.spinner("Processing document..."):

            retriever = build_retriever(
                pdf_path
            )

        st.success("Document processed successfully.")

        st.divider()

        question = st.text_input(
            "Ask a question about the document",
            placeholder="Example: What is software engineering?"
        )

        if st.button("Ask", type="primary"):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Searching the document..."
                ):

                    result = generate_answer(
                        question,
                        retriever
                    )

                st.divider()

                st.markdown("### 💡 Answer")

                st.write(
                    result["answer"]
                )

                if result["sources"]:

                    st.markdown("### 📖 Source")

                    for page in result["sources"]:

                        st.write(
                            f"Page {page}"
                        )

                else:

                    st.info(
                        "No source page was found."
                    )

    finally:

        # Delete temporary PDF after processing
        if os.path.exists(pdf_path):

            os.remove(pdf_path)