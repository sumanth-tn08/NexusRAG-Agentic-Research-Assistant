from app.rag.vector_store import add_document_to_qdrant


def process_uploaded_file(
    file_path: str,
    document_id: str,
    filename: str
):

    chunks = add_document_to_qdrant(
        file_path=file_path,
        document_id=document_id,
        filename=filename
    )

    return chunks