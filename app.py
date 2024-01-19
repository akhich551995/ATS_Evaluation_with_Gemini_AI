from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import io
import os
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## convert the uploaded file (pdf format) to image format
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        #convet to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()
        
        #return the part in base54
        pdf_parts = [ 
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##streamlit App
    
st.set_page_config(page_title = "ATS Resume Evaluation System")
st.header("ATS Resume Evaluation")
input_text = st.text_area("Job Description: ", key = "input")
uploaded_file = st.file_uploader("upload resume (only pdf files)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me about the Resume")

submit2 = st.button("Percentage match with Keywords and missing keywords")

submit3 = st.button("Points can be used to fill that missing skills")

input_prompt1 = """
You are an experienced Human Resource Manager with technical experience in the field of 
Data Science, Bigdata Engineering, Generativeai, Machine learning Engineer and DataAnalyst.Your task is to review the provided resume against the job description
for these provided profiles.
Your task is to share your professional evaluation on the candidate's profile whether it aligns with the job description and 
Highlight the strengths of the candidate as first output and
second output should be the necessary skills to be included in the applicants resume with respect to the job description.
"""

input_prompt2 = """
You are skilled ATS (Applicant Tracking System) scanner with a deep understanding of 
Data Science, Bigdata Engineering, Generativeai, Machine learning Engineer and DataAnalyst and deep ATS functionality,

Your task is to evaluate the resume against the job description and give me the percentage of match if the resume matches
the job description. First output should come as percentage and then Keyword missing as bullet point as second output.
"""

input_prompt3 = """
"As an experienced resume builder with expertise in 
Data Science, Big Data Engineering, Generative AI, Machine Learning Engineering, and Data Analysis, 
your task is to generate sample resume sentences. 
These sentences should highlight the relevant skills and experiences gained from specific projects
listed in the resume. Provide these points with the company's name as the heading, 
emphasizing how the candidate's skills address the missing skills mentioned in the job description. 
This will help tailor the resume to better align with the requirements of potential employers."""


if submit1: 
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Evaluation of the provided resume:")
        st.write(response)
    else:
        st.write("Resume not uploaded")
elif submit2: 
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Percentage match and Keywords missing are:")
        st.write(response)
    else:
        st.write("Resume not uploaded")
elif submit3: 
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Percentage match and Keywords missing are:")
        st.write(response)
    else:
        st.write("Resume not uploaded")