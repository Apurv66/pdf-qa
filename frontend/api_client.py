import requests

API_URL = " http://127.0.0.1:8000"

def get_documents():
    response = requests.get(f"{API_URL}/document")
    response.raise_for_status()

    return response.json()


def upload_document(file):
    response = requests.post(
        f"{API_URL}/document/upload",
        files={
            "file": (
                file.name,
                file,
                "application/pdf"
            )
        }
    )

    response.raise_for_status()
    return response.json()


def ask_question(document_id, question):
    response = requests.post(
        f"{API_URL}/llm/chat",
        json={
            "id": document_id,
            "question": question
        }
    )

    response.raise_for_status()

    return response.json()