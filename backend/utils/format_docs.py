def format_docs(chunks):
    return "\n\n".join(chunk.page_content for chunk in chunks)
