import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json

genai.configure(api_key="AIzaSyAeVPdH7KhfOIQQBUg96OqsAZwn5Xtb9iU")


def get_gemini_repsonse(input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


## streamlit app
st.title("Resume Analysis System")
st.text("Powered by Gemini")
jd = st.text_area("Please paste the job description/job scope")
uploaded_file = st.file_uploader(
    "Upload Your Resume", type="pdf", help="Please upload the resume in pdf format"
)

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = f"""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of various industries. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure \
{{"JD Match":"%", 
"Missing Keywords : []",
"Profile Summary" : ""}}
"""
        response = get_gemini_repsonse(input_prompt)
        st.subheader(response)
