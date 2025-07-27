import streamlit as st
import requests

st.set_page_config(page_title="Document Research & Theme Chatbot", layout="centered")

st.title("📄 Document Research & Theme Chatbot")

# Suggested important questions for the user
st.markdown("""
 Try asking these questions:
- What is the file name?
- What is the title of this document?
- Who is the author or publisher?
- When was it published?
- What type of document is this (report, policy, article)?
- What is the email?
- What is the phone number?
- What is the LinkedIn profile?
- What is the CGPA?
- What is the university?
- What is the graduation year?
- What is the address?
- What are the skills?
- What is the experience?
- What is the education?
- Who is the author?
- What is document about?
- What is the main theme of this document?
- What is the central idea or purpose?
- What problem does this document address?
- What are the main topics covered?
- What are the major sections in this document?
- Is there a summary or conclusion section?
- What are the key facts mentioned in the document?
- What data or statistics are cited?
- What are the main findings or results?
- Define important terms mentioned in the document.
- What is the explanation of [concept]?
- What solutions are suggested in the document?
- What recommendations are made?
- What steps are proposed?
- Give me a summary.
- What is the user's full name?
- What is the user's designation or role?
- What are the user's achievements?
- What certifications does the user have?
- What languages does the user know?
- What are the user's interests or hobbies?
- What is the user's work history?
- What is the user's current employer?
- What is the user's location?
- What is the user's profile summary?
- What is the company name?
- What is the company address?
- What is the company website?
- What is the company contact number?
- Who are the key people in the company?
- What are the company's main products or services?
- What is the company's mission or vision?
- What are the company's achievements?
- What is the company's founding year?
- What is the company's industry or sector?
- What is the company's size or number of employees?
- What awards has the company won?
- What are the company's values
- What is the company's market presence?
- What are the company's recent news or updates?
""")

# Upload PDF
st.subheader("Upload a PDF document")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with open(f"temp/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ File uploaded!")

    # Input field for user question
    question = st.text_input("Ask a question about the document:")

    if st.button("Ask"):
        if question:
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/ask",
                        json={
                            "file_path": f"temp/{uploaded_file.name}",
                            "question": question
                        }
                    )
                    if response.status_code == 200:
                        answer = response.json().get("answer", "No answer found.")
                        st.markdown(f"**Answer:** {answer}")
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"❌ Failed to connect to backend: {e}")
        else:
            st.warning("⚠️ Please enter a question.")

#streamlit run frontend/app.py

