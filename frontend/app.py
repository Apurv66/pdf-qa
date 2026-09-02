import streamlit as st
from api_client import get_documents, upload_document, ask_question

st.title("PDF Q&A")

with st.sidebar:
    st.header("Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        if st.button("Upload"):
            try:
                upload_document(uploaded_file)

                st.success("PDF uploaded successfully!")

                st.rerun()

            except Exception as e:
                st.error(f"Upload failed: {e}")


documents = get_documents()

if documents:
    selected_document = st.selectbox(
        "Select PDF",
        documents,
        format_func=lambda doc: doc["filename"]
    )

    st.write("Selected PDF:", selected_document["filename"])

else:
    st.info("No documents uploaded yet.")


st.subheader("Chat with PDF")

question = st.chat_input("Ask a question about this PDF")

if question:
    try:
        result = ask_question(
            selected_document["id"],
            question
        )

        st.chat_message("user").write(question)

        st.chat_message("assistant").write(
            result["ai_response"]
        )

    except Exception as e:
        st.error(f"Failed to get answer: {e}")