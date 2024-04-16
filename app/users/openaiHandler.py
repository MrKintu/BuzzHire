import json
import logging
import os
import urllib.request

import fitz
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_file_path):
    filename = pdf_file_path[-24:]
    current_directory = os.path.dirname(os.path.abspath(__file__))
    root_directory = current_directory
    while not os.path.exists(os.path.join(root_directory, 'manage.py')):
        root_directory = os.path.dirname(root_directory)
    resumes_directory = os.path.join(root_directory, 'media', 'resumes')
    resume_path = ""
    # Iterate through the files in the "resumes" directory
    for file_name in os.listdir(resumes_directory):
        # Check if the filename matches the target filename
        if file_name == filename:
            # If a match is found, return the absolute filepath
            resume_path = os.path.join(resumes_directory, file_name)

    # Open the PDF file
    with open(resume_path, 'rb') as file:
        pdf_document = fitz.open(file)
        # Extract text from each page
        text = ''
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

    return text


def ReadResume(resume_pdf):
    env = os.environ
    API_URL = env.get('API_URL')
    API_KEY = env.get('API_KEY')

    # Extract text from PDF
    resume_text = extract_text_from_pdf(resume_pdf)

    url = f"{API_URL}/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-07-01-preview&api-key={API_KEY}"
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI HR that creates a valid json with the following attributes in brief- name, "
                           "email, contact_number, linkedin_profile, all_skills(no subattributes), "
                           "education(degree, university, start_year in python datetime format, "
                           "end_year in python datetime format, gpa), roles(title, company, location, "
                           "start_date in python datetime format, end_date in python datetime format, "
                           "responsibilities). Strictly stick to the given attributes and sub-attributes only. "
                           "If information is absent, say N/A. If any of the dates aren't in full YYYY-MM-DD format,"
                           "assume that the date starts on the 1st day of the specified month. If any of the dates"
                           "are missing information about the associated month, then say N/A. "
                           "The attributes all_skills, education and roles should be returned as a python list."
            },
            {
                "role": "user",
                "content": resume_text
            }
        ],
        "temperature": 0.5,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 4000
    }
    data = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(url, data=data, method="POST", headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(request)

    status_code = response.getcode()
    if status_code == 200:
        # Process the response
        response = response.read().decode("utf-8")
        result = json.loads(response)
        result = json.loads(result['choices'][0]['message']['content'].replace("\n", ""))
        logger.info(str(result))
    else:
        result = False

    return result
