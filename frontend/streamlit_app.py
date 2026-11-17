
import streamlit as st
import requests

# ==========================================
# CONFIGURATION
# ==========================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Document Intelligence Assistant",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "documents" not in st.session_state:
    st.session_state.documents = []

if "selected_document_id" not in st.session_state:
    st.session_state.selected_document_id = None

if "messages_by_document" not in st.session_state:
    st.session_state.messages_by_document = {}


# ==========================================
# BACKEND FUNCTIONS
# ==========================================

def fetch_documents():
    """Retrieve all registered documents from SQLite."""

    try:
        response = requests.get(
            f"{API_URL}/documents",
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        st.session_state.documents = data.get(
            "documents", []
        )

        return True

    except requests.exceptions.RequestException as error:
        st.error(f"Unable to load documents: {error}")
        return False


def upload_pdf(uploaded_file):
    """Upload one PDF to the FastAPI backend."""

    response = requests.post(
        f"{API_URL}/upload",
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()


def ask_document(document_id, question):
    """Send a question to the RAG API."""

    response = requests.post(
        f"{API_URL}/ask",
        json={
            "document_id": document_id,
            "question": question
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()


def get_chat_history(document_id):
    """Get chat history for a particular document."""

    if document_id not in st.session_state.messages_by_document:
        st.session_state.messages_by_document[document_id] = []

    return st.session_state.messages_by_document[document_id]


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("📄 AI Document Intelligence Assistant")

st.markdown(
    """
    Upload multiple PDF documents and ask questions using
    **Retrieval-Augmented Generation (RAG)**.

    Your uploaded documents remain available through the
    persistent document library.
    """
)

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("📁 Document Manager")

    # Multiple PDF uploader

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can select multiple PDF files."
    )

    if st.button(
        "Upload Selected PDFs",
        disabled=not uploaded_files,
        use_container_width=True
    ):

        successful_uploads = 0
        failed_uploads = 0

        progress = st.progress(0)

        status = st.empty()

        total_files = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):

            status.info(
                f"Processing {index + 1}/{total_files}: "
                f"{uploaded_file.name}"
            )

            try:
                result = upload_pdf(uploaded_file)

                successful_uploads += 1

                # Initialize chat history for new document
                document_id = result["document_id"]

                st.session_state.messages_by_document.setdefault(
                    document_id, []
                )

                # Select the latest uploaded document
                st.session_state.selected_document_id = document_id

                st.success(
                    f"Uploaded: {result['filename']} "
                    f"({result['total_pages']} pages, "
                    f"{result['total_chunks']} chunks)"
                )

            except requests.exceptions.RequestException as error:

                failed_uploads += 1

                st.error(
                    f"Failed to upload {uploaded_file.name}: {error}"
                )

            except (KeyError, ValueError) as error:

                failed_uploads += 1

                st.error(
                    f"Unexpected upload response for "
                    f"{uploaded_file.name}: {error}"
                )

            progress.progress((index + 1) / total_files)

        status.empty()

        st.write(
            f"**Successful:** {successful_uploads} | "
            f"**Failed:** {failed_uploads}"
        )

        # Refresh persistent document library
        fetch_documents()

        st.rerun()

    st.divider()

    # Document library

    st.subheader("📚 Document Library")

    if st.button(
        "🔄 Refresh Library",
        use_container_width=True
    ):
        fetch_documents()

    documents = st.session_state.documents

    if documents:

        document_ids = [
            document["document_id"]
            for document in documents
        ]

        # Keep selection valid
        if st.session_state.selected_document_id not in document_ids:
            st.session_state.selected_document_id = document_ids[0]

        def document_label(document_id):
            document = next(
                item for item in documents
                if item["document_id"] == document_id
            )

            return document["filename"]

        selected_document_id = st.selectbox(
            "Select a document to chat with",
            options=document_ids,
            format_func=document_label,
            key="document_selector"
        )

        st.session_state.selected_document_id = selected_document_id

        selected_document = next(
            document for document in documents
            if document["document_id"] == selected_document_id
        )

        st.success("Document ready")

        st.write(f"**Filename:** {selected_document['filename']}")

        st.write(
            f"**Pages:** {selected_document.get('total_pages', 'N/A')}"
        )

        st.write(
            f"**Chunks:** {selected_document.get('total_chunks', 'N/A')}"
        )

        with st.expander("Document details"):
            st.code(selected_document_id)

            st.write(
                f"**Uploaded:** "
                f"{selected_document.get('uploaded_at', 'Unknown')}"
            )

        if st.button(
            "Clear current chat",
            use_container_width=True
        ):
            st.session_state.messages_by_document[
                selected_document_id
            ] = []

            st.rerun()

    else:
        st.info(
            "No documents found. Upload your first PDF to get started."
        )


# ==========================================
# MAIN CHAT INTERFACE
# ==========================================

st.subheader("💬 Chat with your documents")

selected_id = st.session_state.selected_document_id

if not selected_id:

    st.info(
        "Upload a PDF or select an existing document "
        "from the sidebar to start chatting."
    )

else:

    selected_document = next(
        (
            document for document in st.session_state.documents
            if document["document_id"] == selected_id
        ),
        None
    )

    if selected_document:

        st.caption(
            f"Currently chatting with: "
            f"{selected_document['filename']}"
        )

    messages = get_chat_history(selected_id)

    # Display chat history

    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("sources"):

                with st.expander("📖 View source references"):

                    for source in message["sources"]:

                        st.markdown(
                            f"**Page {source['page_number']}**"
                        )

                        st.write(source["content"])

                        st.divider()

    # User question input

    question = st.chat_input(
        "Ask something about your selected PDF..."
    )

    if question:

        # Save and display user question

        messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Generate AI response

        with st.chat_message("assistant"):

            try:

                with st.spinner("AI is analyzing your document..."):

                    result = ask_document(
                        selected_id,
                        question
                    )

                answer = result["answer"]

                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:

                    with st.expander("📖 View source references"):

                        for source in sources:

                            st.markdown(
                                f"**Page {source['page_number']}**"
                            )

                            st.write(source["content"])

                            st.divider()

                messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.exceptions.RequestException as error:

                error_message = (
                    f"Unable to connect to backend: {error}"
                )

                st.error(error_message)

                messages.append({
                    "role": "assistant",
                    "content": error_message
                })

            except (KeyError, ValueError) as error:

                error_message = (
                    f"Unexpected API response: {error}"
                )

                st.error(error_message)

                messages.append({
                    "role": "assistant",
                    "content": error_message
                })
