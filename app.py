from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from docx import Document
import re
import os

app = Flask(__name__)

# Function to extract information (use your existing function)
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
        # Add more fields as necessary
    }

    # Replace problematic sequences
    doc_text = doc_text.replace("=-", "-")
    doc_text = doc_text.replace("=", "")

    for key in data.keys():
        pattern = rf'{key}\s*:\s*(.*?)(?=\n[A-Z][a-z\s]*\s*:\s*|\Z)'
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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        custom_filter = request.form.get('custom_filter')

        # Process file upload
        if file and file.filename.endswith('.docx'):
            filename = secure_filename(file.filename)
            filepath = os.path.join('', filename)
            file.save(filepath)
            document = Document(filepath)
            doc_text = '\n'.join([para.text for para in document.paragraphs])
        else:
            return 'No file provided'

        # Extract information from the text
        data = extract_information(doc_text)

        # Apply custom filter if specified
        if custom_filter:
            filter_key = custom_filter.strip()
            pattern = rf'{filter_key}\s*:\s*(.*?)(?=\n[A-Z][a-z\s]*\s*:\s*|\Z)'
            matches = re.findall(pattern, doc_text, re.DOTALL)
            extracted_values = [match.strip() for match in matches]
            if len(extracted_values) > 0:
                data[filter_key] = extracted_values + [''] * (len(data['Case Code']) - len(extracted_values))
            else:
                data[filter_key] = [''] * len(data['Case Code'])

        df = pd.DataFrame(data)
        excel_path = 'output.xlsx'
        df.to_excel(excel_path, index=False)
        return send_file(excel_path, as_attachment=True)

    return '''
    <!doctype html>
    <title>Upload Document and Apply Filter</title>
    <h1>Upload Document and Apply Filter</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <br><br>
      <!-- Inputs for filters -->
      <label for="custom_filter">Custom Filter (e.g., Test):</label>
      <input type="text" name="custom_filter" placeholder="Enter custom filter">
      <br><br>
      <input type="submit" value="Upload">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
