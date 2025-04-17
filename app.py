# import streamlit as st
# import fitz  # PyMuPDF
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Set page configuration first
# st.set_page_config(page_title="ATS Resume Analyzer with Gemini AI", layout="wide")

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Function to extract text from uploaded PDF
# def extract_text_from_pdf(uploaded_file):
#     doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# # Function to call Gemini API
# def get_gemini_response(role_prompt, pdf_text, user_question):
#     try:
#         model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")  # Update with correct model
#         response = model.generate_content([role_prompt, pdf_text, user_question])
#         return response.text
#     except Exception as e:
#         st.error(f"Error during API request: {e}")
#         return "An error occurred while processing your request."

# # Streamlit App UI
# st.title("🤖 ATS Resume Analyzer with Gemini AI")

# # Upload resume
# uploaded_file = st.file_uploader("📄 Upload your resume (PDF only)", type="pdf")

# # Job Description input
# input_text = st.text_area("📝 Enter the Job Description:")

# # Prompts
# role_prompt = """
# You are an experienced HR with technical expertise in Data Science, Web Development, Big Data, DevOps, and Data Analytics. 
# Evaluate the following resume based on the provided job description and give a detailed analysis.
# """

# improve_prompt = """
# You are a career advisor. Based on the resume and job description, give suggestions on how the candidate can improve their skills to better match the job.
# """

# match_prompt = """
# You are an ATS system. Analyze the resume against the job description and give:
# 1. Match Percentage
# 2. Missing Keywords
# 3. Final Conclusion
# """

# # Buttons
# col1, col2, col3 = st.columns(3)
# with col1:
#     submit1 = st.button("📌 Resume Evaluation")
# with col2:
#     submit2 = st.button("🔧 Skill Improvement")
# with col3:
#     submit3 = st.button("📊 Match Percentage")

# # When any button is clicked
# if uploaded_file:
#     pdf_text = extract_text_from_pdf(uploaded_file)

#     if submit1:
#         with st.spinner("Analyzing resume..."):
#             response = get_gemini_response(role_prompt, pdf_text, input_text)
#             st.subheader("📝 Resume Evaluation")
#             st.write(response)

#     elif submit2:
#         with st.spinner("Generating skill suggestions..."):
#             response = get_gemini_response(improve_prompt, pdf_text, input_text)
#             st.subheader("💡 Skill Improvement Suggestions")
#             st.write(response)

#     elif submit3:
#         with st.spinner("Calculating match..."):
#             response = get_gemini_response(match_prompt, pdf_text, input_text)
#             st.subheader("📊 Match Report")
#             st.write(response)
# else:
#     st.warning("⚠️ Please upload a PDF resume to proceed.")

import streamlit as st
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page configuration first
st.set_page_config(page_title="ATS Resume Analyzer with Gemini AI", layout="wide")

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to call Gemini API
def get_gemini_response(role_prompt, pdf_text, user_question):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        response = model.generate_content([role_prompt, pdf_text, user_question])
        return response.text
    except Exception as e:
        st.error(f"Error during API request: {e}")
        return "An error occurred while processing your request."

# Streamlit App UI
st.title("🤖 ATS Resume Analyzer with Gemini AI")
st.markdown("<hr>", unsafe_allow_html=True)

# Create a layout with columns for better structure
col1, col2 = st.columns([2, 3])
with col1:
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")
    if uploaded_file is not None:
        st.success("✅ PDF Uploaded Successfully")
    else:
        st.warning("⚠️ Please upload a PDF resume.")

with col2:
    st.subheader("📝 Enter the Job Description")
    input_text = st.text_area("Paste the job description here...", height=200, help="Enter the full job description.")

# Section for buttons (in a single row with a bit of spacing between them)
col1, col2, col3 = st.columns(3)
with col1:
    submit1 = st.button("📌 Resume Evaluation")
with col2:
    submit2 = st.button("🔧 Skill Improvement")
with col3:
    submit3 = st.button("📊 Match Percentage")

# Results Section
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)

    # When a button is clicked, show appropriate results
    if submit1:
        with st.spinner("Analyzing resume..."):
            response = get_gemini_response(role_prompt="Evaluate the resume based on the job description.", pdf_text=pdf_text, user_question=input_text)
            st.subheader("📝 Resume Evaluation Results")
            st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: #E0F7FA; color: #00796B;'>{response}</div>", unsafe_allow_html=True)

    elif submit2:
        with st.spinner("Generating skill suggestions..."):
            response = get_gemini_response(role_prompt="Give suggestions for skills improvement.", pdf_text=pdf_text, user_question=input_text)
            st.subheader("💡 Skill Improvement Suggestions")
            st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: #FFF9C4; color: #F57F17;'>{response}</div>", unsafe_allow_html=True)

    elif submit3:
        with st.spinner("Calculating match..."):
            response = get_gemini_response(role_prompt="Match the resume with the job description, with Match Percentage", pdf_text=pdf_text, user_question=input_text)
            st.subheader("📊 Match Percentage Results")
            st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: #C8E6C9; color: #388E3C;'>{response}</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ Please upload a PDF resume to proceed.")

# Footer Section (optional, for app branding)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Made with ❤️ by Sai Magar | [GitHub](https://github.com/Sai-Magar)", unsafe_allow_html=True)
