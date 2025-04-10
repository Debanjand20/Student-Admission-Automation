import streamlit as st
import json
from agents.document_checker import run_doc_check
from agents.shortlister import run_shortlisting
from agents.loan_agent import run_loan_check
from agents.admission_letter import run_admission_letter
from agents.director_bot import run_director_query
from utils.pdf_generator import generate_admission_letter_pdf
from utils.report_generator import generate_summary_report
from utils.email_sender import send_admission_email
from vector_store import load_and_embed_documents

st.set_page_config(page_title="🎓 Student Admission Automation", layout="centered")
st.title("🎓 Automated Helpdesk for Student Admissions")

st.markdown("#### 👇 Start by embedding admission policy documents")

if st.button("📚 Embed Admission Documents"):
    load_and_embed_documents()
    st.success("✅ Admission documents embedded into ChromaDB.")

st.markdown("---")
st.subheader("📥 Upload Student Application")

uploaded_file = st.file_uploader("Upload Application JSON", type="json")

if uploaded_file:
    application = json.load(uploaded_file)
    st.json(application)

    if st.button("⚙️ Run Admission Process"):
        with st.spinner("Verifying documents..."):
            doc_result = run_doc_check(application)
            st.info(f"📄 Document Check:\n{doc_result}")

        with st.spinner("Checking eligibility..."):
            shortlist_result = run_shortlisting(application)
            st.info(f"🎯 Shortlisting:\n{shortlist_result}")

        with st.spinner("Processing loan request..."):
            loan_result = run_loan_check(application)
            st.info(f"💰 Loan Decision:\n{loan_result}")

        with st.spinner("Generating admission letter..."):
            letter = run_admission_letter(application)
            st.code(letter, language="markdown")

            pdf_path = generate_admission_letter_pdf(application, {
                "tuition": 50000,
                "hostel": 30000,
                "exam": 5000
            })
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Admission Letter (PDF)",
                    data=f,
                    file_name=pdf_path.split("/")[-1],
                    mime="application/pdf"
                )

        if "email" in application:
            if st.button("📤 Send Admission Email"):
                success = send_admission_email(
                    to_email=application["email"],
                    student_name=application["name"],
                    letter_text=letter,
                    pdf_path=pdf_path
                )
                if success:
                    st.success(f"✅ Email sent to {application['email']}")
                else:
                    st.error("❌ Failed to send email.")

st.markdown("---")
st.subheader("👨‍💼 University Director Chatbot")

query = st.text_input("Ask about admission stats (e.g. 'How many students admitted?')")

if query:
    response = run_director_query(query)
    st.success(response)

st.markdown("---")
st.subheader("📑 Download Admission Summary Report")

if st.button("📄 Generate Report"):
    report = generate_summary_report()
    st.code(report, language="markdown")
    st.download_button("📥 Download Report", report, file_name="admission_summary.txt")
