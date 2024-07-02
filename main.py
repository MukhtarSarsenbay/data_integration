import pandas as pd
from docx import Document
import re

def extract_information(doc_text):
    # Example of the structured content
    data = {
        'Case Code': [],
        'Homepage Vignette': [],
        'Individual Page Vignette': [],
        'Patient Name': [],
        'Age': [],
        'Location': [],
        'Personality': [],
        'Presenting Complaint': [],
        'Quote': [],
        'Symptoms': [],
        'PV Bleeding': [],
        'PV Discharge': [],
        'Abdominal or Pelvic Pain': [],
        'Chance of Pregnancy': [],
        'Dyspareunia': [],
        'Post-coital PV Bleeding': [],
        'Intermenstrual PV Bleeding': [],
        'Post-menopausal Bleeding': [],
        'Vulval skin changes or itching': [],
        'Abdominal distention': [],
        'Quote_2': [],
        'History of Presenting Complaint': [],
        'Systemic Symptoms': [],
        'Obstetric History': [],
        'Gynaecology History': [],
        'Past Medical History': [],
        'Drug History': [],
        'Allergies': [],
        'Family History': [],
        'Social History': [],
        'Sexual History': [],
        'Travel History': [],
        'Ideas, Concerns, and Expectations': [],
        'Observations': [],
        'Physical Examination': [],
        'Diagnostic Tests': [],
        'Treatment': [],
        'Monitoring': [],
        'Prognosis': [],
        'Differential diagnoses': [],
        'Keyword Filters': [],
        'Speciality Filter': [],
        'Presenting Complaint Filter': [],
        'Condition Filter': [],
        'Location Filter': [],
        'Case created by': [],
        'Reviewed by': [],
    }

    # Replace problematic sequences
    doc_text = doc_text.replace("=-", "-")
    doc_text = doc_text.replace("=", "")

    for key in data.keys():
        pattern = rf'{key}:(.*?)(?=\n[A-Z][a-z\s]*:|\Z)'
        matches = re.findall(pattern, doc_text, re.DOTALL)
        if matches:
            data[key].extend([match.strip() for match in matches])
        else:
            data[key].append('')

    # Ensure all lists in the dictionary have the same length
    max_length = max(len(lst) for lst in data.values())
    for key in data.keys():
        while len(data[key]) < max_length:
            data[key].append('')

    return data

# Load the .docx file
doc = Document('case_doc_full.docx')
doc_text = '\n'.join([para.text for para in doc.paragraphs])

# Extract the information
data = extract_information(doc_text)

# Convert the extracted information into a pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

df.to_excel('case_information.xlsx', index=False)

