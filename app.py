from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from docx import Document
import re
import os

app = Flask(__name__)

# Function to extract information (use your existing function)
def extract_information(doc_text, specific_name):
    data = {
        'general': {
        'Case_Code': [],
        'Homepage_Vignette': [],
        'Individual_Page_Vignette': [],
        'Name': [],
        'Date_of_Birth': [],
        'Location': [],
        'Personality': [],
        'Presenting_Complaint': [],
        'Presenting_Complaint_Quote': [],
        'Symptoms': [],
        'Symptoms_Quote': [],
        'History_of_Presenting_Complaint': [],
        'History_of_Presenting_Complaint_Quote': [],
        'Systemic_Symptoms': [],
        'Systemic_Symptoms_Quote': [],
        'Obstetric_History': [],
        'Gynaecology_History': [],
        'Gynaecology_History_Quote': [],
        'Past_Medical_History': [],
        'Past_Medical_History_Quote': [],
        'Drug_History': [],
        'Drug_History_Quote': [],
        'Allergies': [],
        'Allergies_Quote': [],
        'Family_History': [],
        'Family_History_Quote': [],
        'Social_History': [],
        'Social_History_Quote': [],
        'Ideas_Concerns_and_Expectations': [],
        'Ideas_Concerns_and_Expectations_Quote': [],
        'Observations': [],
        'Physical_Examination': [],
        'Diagnostic_Tests': [],
        'Treatment': [],
        'Monitoring': [],
        'Prognosis': [],
        'Differential_Diagnoses': [],
        'Keyword_Filters': [],
        'Case_created_by': [],
        'Reviewed_by': [],
        'Test': []
    },
        'cancer': {
            'Case_Code': [],
            'Homepage_Vignette': [],
            'Individual_Page_Vignette': [],
            'Name': [],
            'Date_of_Birth': [],
            'Location': [],
            'Personality': [],
            'Presenting_Complaint': [],
            'Presenting_Complaint_Quote': [],
            'Symptoms': [],
            'Symptoms_Quote': [],
            'History_of_Presenting_Complaint': [],
            'History_of_Presenting_Complaint_Quote': [],
            'Systemic_Symptoms': [],
            'Systemic_Symptoms_Quote': [],
            'Past_Medical_History': [],
            'Past_Medical_History_Quote': [],
            'Drug_History': [],
            'Drug_History_Quote': [],
            'Allergies': [],
            'Allergies_Quote': [],
            'Family_History': [],
            'Family_History_Quote': [],
            'Social_History': [],
            'Social_History_Quote': [],
            'Ideas_Concerns_and_Expectations': [],
            'Ideas_Concerns_and_Expectations_Quote': [],
            'Observations': [],
            'Physical_Examination': [],
            'Diagnostic_Tests': [],
            'Condition': [],
            'Patient_Questions': [],
            'Examiner_Questions': [],
            'Treatment': [],
            'Monitoring': [],
            'Prognosis': [],
            'Differential_Diagnoses': [],
            'Filter_Specialties': [],
            'Filter_Presenting_Complaints': [],
            'Filter_Condition': [],
            'Filter_Location': [],
            'Filter_Scenerio': [],
            'Case_created_by': [],
            'Reviewed_by_1': [],
            'Reviewed_by_2': [],
            'RegistedUser?': [],
            'Media?': [],
            'Location_of_Media': []
        }
    }

    doc_text = doc_text.replace("=-", "-").replace("=", "")

    current_data = data.get(specific_name, data['general'])

    patterns = {
        'Case_Code': r'Case\s*Code\s*:\s*(\w+_\d+_[A-Za-z]+)\s*(?=\nHomepage\s*Vignette\s*:\s*|\Z)',
        'Homepage_Vignette': r'Homepage\s*Vignette\s*:\s*(.*?)(?=\nIndividual\s*Page\s*Vignette\s*:\s*|\Z)',
        'Individual_Page_Vignette': r'Individual\s*Page\s*Vignette\s*:\s*(.*?)(?=\nPatient\s*Name\s*:\s*|\Z)',
        'Name': r'Patient\s*Name\s*:\s*(.*?)(?=\nAge\s*:\s*|\Z)',
        'Date_of_Birth': r'Age\s*:\s*(.*?)(?=\nLocation\s*:\s*|\Z)',
        'Location': r'Location\s*:\s*(.*?)(?=\nPersonality\s*:\s*|\Z)',
        'Personality': r'Personality\s*:\s*(.*?)(?=\nPresenting\s*Complaint\s*:\s*|\Z)',
        'Presenting_Complaint': r'Presenting\s*Complaint\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Presenting_Complaint_Quote': r'Quote\s*:\s*(.*?)(?=\nSymptoms\s*:\s*|\Z)',
        'Symptoms': r'Symptoms\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Symptoms_Quote': r'Symptoms\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nHistory\s*of\s*Presenting\s*Complaint\s*:\s*|\Z)',
        'History_of_Presenting_Complaint': r'History\s*of\s*Presenting\s*Complaint\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'History_of_Presenting_Complaint_Quote': r'History\s*of\s*Presenting\s*Complaint\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nSystemic\s*Symptoms\s*:\s*|\Z)',
        'Systemic_Symptoms': r'Systemic\s*Symptoms\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Systemic_Symptoms_Quote': r'Systemic\s*Symptoms\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nObstetric\s*History\s*:\s*|\Z)',
        'Obstetric_History': r'Obstetric\s*History\s*:\s*(.*?)(?=\nGynaecology\s*History\s*:\s*|\Z)',
        'Gynaecology_History': r'Gynaecology\s*History\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Gynaecology_History_Quote': r'Gynaecology\s*History\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nPast\s*Medical\s*History\s*:\s*|\Z)',
        'Past_Medical_History': r'Past\s*Medical\s*History\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Past_Medical_History_Quote': r'Past\s*Medical\s*History\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nDrug\s*History\s*:\s*|\Z)',
        'Drug_History': r'Drug\s*History\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Drug_History_Quote': r'Drug\s*History\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nAllergies\s*:\s*|\Z)',
        'Allergies': r'Allergies\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Allergies_Quote': r'Allergies\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nFamily\s*History\s*:\s*|\Z)',
        'Family_History': r'Family\s*History\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Family_History_Quote': r'Family\s*History\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nSocial\s*History\s*:\s*|\Z)',
        'Social_History': r'Social\s*History\s*:\s*(.*?)(?=\nQuote\s*:\s*|\Z)',
        'Social_History_Quote': r'Social\s*History\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nIdeas\s*,\s*Concerns\s*,\s*and\s*Expectations\s*:\s*|\Z)',
        'Ideas_Concerns_and_Expectations': r'Ideas\s*,\s*Concerns\s*,\s*and\s*Expectations\s*:\s*(.*?)(?=\n[A-Z][a-z\s]*\s*:\s*|\Z)',
        'Ideas_Concerns_and_Expectations_Quote': r'Ideas\s*,\s*Concerns\s*,\s*and\s*Expectations\s*:\s*(?:.|\n)*?\nQuote\s*:\s*(.*?)(?=\nObservations\s*:\s*|\Z)',
        'Observations': r'Observations\s*:\s*(.*?)(?=\nPhysical\s*Examination\s*:\s*|\Z)',
        'Physical_Examination': r'Physical\s*Examination\s*:\s*(.*?)(?=\nDiagnostic\s*Tests\s*:\s*|\Z)',
        'Diagnostic_Tests': r'Diagnostic\s*Tests\s*:\s*(.*?)(?=\nTreatment\s*:\s*|\Z)',
        'Treatment': r'Treatment\s*:\s*(.*?)(?=\nMonitoring\s*:\s*|\Z)',
        'Monitoring': r'Monitoring\s*:\s*(.*?)(?=\nPrognosis\s*:\s*|\Z)',
        'Prognosis': r'Prognosis\s*:\s*(.*?)(?=\nDifferential\s*diagnoses\s*:\s*|\Z)',
        'Differential_Diagnoses': r'Differential\s*Diagnoses\s*:\s*(.*?)(?=\nKeyword\s*Filters\s*:\s*|\Z)',
        'Keyword_Filters': r'Keyword\s*Filters\s*:\s*(.*?)(?=\nCase\s*created\s*by\s*:\s*|\Z)',
        'Case_created_by': r'Case\s*created\s*by\s*:\s*(.*?)(?=\nReviewed\s*by\s*:\s*|\Z)',
        'Reviewed_by': r'Reviewed\s*by\s*:\s*(.*?)(?=\nTest\s*:\s*|\Z)',
        'Test': r'Test\s*:\s*(.*?)(?=\nCase\s*Code\s*:\s*|\Z)',
    }

    for key, pattern in patterns.items():
        matches = re.findall(pattern, doc_text, re.DOTALL)
        for match in matches:
            current_data[key].append(match.strip())

    max_length = max(len(lst) for lst in current_data.values())
    for key in current_data.keys():
        while len(current_data[key]) < max_length:
            current_data[key].append('')

    return current_data

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        specific_name = request.form.get('specific_name')
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
        data = extract_information(doc_text, specific_name)

        # Apply custom filter if specified
        if custom_filter:
            filter_key = custom_filter.strip()
            pattern = rf'{filter_key}\s*:\s*(.*?)(?=\n[A-Z][a-z\s]*\s*:\s*|\Z)'
            matches = re.findall(pattern, doc_text, re.DOTALL)
            extracted_values = [match.strip() for match in matches]
            if len(extracted_values) > 0:
                data[filter_key] = extracted_values + [''] * (len(data['Case_Code']) - len(extracted_values))
            else:
                data[filter_key] = [''] * len(data['Case_Code'])

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
      <!-- Input for specific name -->
      <label for="specific_name">Specific Name:</label>
      <select name="specific_name">
        <option value="general">General</option>
        <option value="cancer">Cancer</option>
        <!-- Add more specific names as necessary -->
      </select>
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
