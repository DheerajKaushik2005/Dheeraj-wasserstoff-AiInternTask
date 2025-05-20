import streamlit as st
from streamlit import markdown
import os
from backend.app.services import ingest, embed, query, summarize

if "docs" not in st.session_state:
    st.session_state.docs = None

if "theme" not in st.session_state:
    st.session_state.theme = None

if "history" not in st.session_state:
    st.session_state.history = []


st.title("🧠 Document Research Assistant")
uploaded_files = st.file_uploader(
    "Upload image(s) or PDF(s)",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("data/input_images", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("data/input_images", file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())

    st.success("✅ Images uploaded successfully.")
    st.write("🔍 Extracting text...")
    ingest.process_files("data/input_images", "data/text_outputs")

    st.write("📚 Embedding documents...")
    docs = embed.load_texts("data/text_outputs")
    embed.embed_documents(docs)
    st.session_state.docs = docs  # ⬅️ Store in session
    st.success("✅ Documents embedded!")

    if st.button("🔎 Summarize Theme"):
        full_text = "\n".join([doc.page_content for doc in docs])
        summary = summarize.get_theme_summary(full_text)
        st.session_state.theme = summary  # ⬅️ Save it
        st.success("✅ Theme extracted!")


    # 🔍 Q&A Section
    # Theme summary (always shown if exists)
    if st.session_state.theme:
        st.markdown("### 🧩 Theme Summary")
        st.info(st.session_state.theme)

    st.divider()

    # Ask a question
    st.markdown("### 💬 Ask a Question")
    query_text = st.text_input("🔍 Type your question")

    col1, col2 = st.columns([1, 5])
    with col1:
        ask_clicked = st.button("Ask", use_container_width=True)
    with col2:
        clear_clicked = st.button("🧹 Clear History", use_container_width=True)

    # Ask a question
    if ask_clicked and query_text:
        with st.spinner("🤖 Thinking..."):
            answer = query.ask_question(query_text)
        st.session_state.history.append((query_text, answer))

    # Clear chat
    if clear_clicked:
        st.session_state.history.clear()

    # Show history
    if st.session_state.history:
        st.markdown("### 📜 Q&A History")
        for i, (q, a) in enumerate(st.session_state.history[::-1], 1):
            st.markdown(f"""
    <div style="background-color:#1e1e1e;padding:1rem;border-radius:8px;margin-bottom:1rem">
    <b style="color:#f39c12">Q{i}:</b> {q}<br>
    <b style="color:#2ecc71">A:</b> {a}
    </div>
    """, unsafe_allow_html=True)
