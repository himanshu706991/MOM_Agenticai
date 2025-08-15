import streamlit as st
from io import BytesIO
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import PyPDF2
import docx2txt

# --------- Function to extract text ---------
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)
    else:
        return None

# --------- Function to generate MoM ---------
def generate_minutes_of_meeting(transcript):
    # This is a template — adjust sections as needed
    mom_text = f"""
Minutes of Meeting (MoM)
========================

Date: __________
Meeting Title: __________
Participants: __________

Agenda:
-------
- [List agenda items here]

Discussion Summary:
-------------------
{transcript.strip()}

Key Decisions:
--------------
- Decision 1
- Decision 2

Action Items:
-------------
| Action Item | Responsible Person | Due Date |
|-------------|-------------------|----------|
| Example     | John Doe           | DD/MM/YY |

Next Steps:
-----------
- Step 1
- Step 2

Meeting Closed at: __________

Prepared By: __________
Approved By: __________
"""
    return mom_text

# --------- Function to download Word ---------
def download_word(mom_text):
    doc = Document()
    for line in mom_text.split("\n"):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --------- Function to download PDF ---------
def download_pdf(mom_text):
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(buffer)
    paragraphs = [Paragraph(line, styles["Normal"]) for line in mom_text.split("\n")]
    doc.build(paragraphs)
    buffer.seek(0)
    return buffer

# --------- Streamlit UI ---------
st.set_page_config(page_title="Minutes of Meeting Generator", layout="wide")

st.title("📄 Minutes of Meeting Generator")
st.write("Upload your meeting transcript to generate a formal MoM document.")

uploaded_file = st.file_uploader("Upload Transcript File", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    transcript = extract_text_from_file(uploaded_file)
    if transcript:
        mom_text = generate_minutes_of_meeting(transcript)

        st.subheader("Generated Minutes of Meeting")
        st.text_area("Minutes of Meeting", mom_text, height=400)

        col1, col2 = st.columns(2)

        with col1:
            word_data = download_word(mom_text)
            st.download_button("📥 Download as Word", word_data, file_name="Minutes_of_Meeting.docx")

        with col2:
            pdf_data = download_pdf(mom_text)
            st.download_button("📥 Download as PDF", pdf_data, file_name="Minutes_of_Meeting.pdf")
    else:
        st.error("Could not extract text from the uploaded file. Please try another format.")
