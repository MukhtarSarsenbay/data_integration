# def extract_information(doc_text):
#     patterns = {
#         'Case_Code': r'Case_Code[:\s]*([A-Za-z0-9_-]+)',  # Extracts alphanumeric code
#         'Homepage_Vignette': r'Homepage_Vignette[:\s]*(.*?)\s*(?=\b(Individual_Page_Vignette|Name|Date of Birth|$))',
#         'Individual_Page_Vignette': r'Individual_Page_Vignette[:\s]*(.*?)\s*(?=\b(Name|Date of Birth|$))',
#         'Name': r'Name[:\s]*(.*?)\s*(?=\b(Date of Birth|Location|$))',
#         'Date of Birth': r'Date of Birth[:\s]*(.*?)\s*(?=\b(Location|Personality|$))',
#         'Location': r'Location[:\s]*(.*?)\s*(?=\b(Personality|Presenting_Complaint|$))',
#         'Personality': r'Personality[:\s]*(.*?)\s*(?=\b(Presenting_Complaint|Presenting_Complaint_Quote|$))',
#         'Presenting_Complaint': r'Presenting_Complaint[:\s]*(.*?)\s*(?=\b(Presenting_Complaint_Quote|Symptoms|$))',
#         'Presenting_Complaint_Quote': r'Presenting_Complaint_Quote[:\s]*"(.*?)"\s*(?=\b(Symptoms|Symptoms_Quote|$))',
#         'Symptoms': r'Symptoms[:\s]*(.*?)\s*(?=\b(Symptoms_Quote|History_of_Presenting_Complaint|$))',
#         'Symptoms_Quote': r'Symptoms_Quote[:\s]*"(.*?)"\s*(?=\b(History_of_Presenting_Complaint|Systemic_Symptoms|$))',
#         'History_of_Presenting_Complaint': r'History_of_Presenting_Complaint[:\s]*(.*?)\s*(?=\b(Systemic_Symptoms|Systemic_Symptoms_Quote|$))',
#         'Systemic_Symptoms': r'Systemic_Symptoms[:\s]*(.*?)\s*(?=\b(Obstetric_History|Obstetric_History_Quote|$))',
#         'Obstetric_History': r'Obstetric_History[:\s]*(.*?)\s*(?=\b(Gynaecology_History|Past_Medical_History|$))',
#         'Past_Medical_History': r'Past_Medical_History[:\s]*(.*?)\s*(?=\b(Drug_History|$))',
#         'Drug_History': r'Drug_History[:\s]*(.*?)\s*(?=\b(Allergies|$))',
#         'Allergies': r'Allergies[:\s]*(.*?)\s*(?=\b(Family_History|$))',
#         'Family_History': r'Family_History[:\s]*(.*?)\s*(?=\b(Social_History|$))',
#         'Social_History': r'Social_History[:\s]*(.*?)\s*(?=\b(Sexual_History|$))',
#         'Sexual_History': r'Sexual_History[:\s]*(.*?)\s*(?=\b(Ideas_Concerns_and_Expectations|$))',
#         'Ideas_Concerns_and_Expectations': r'Ideas_Concerns_and_Expectations[:\s]*(.*?)\s*(?=\b(Observations|$))',
#         'Observations': r'Observations[:\s]*(.*?)\s*(?=\b(Physical_Examination|$))',
#         'Physical_Examination': r'Physical_Examination[:\s]*(.*?)\s*(?=\b(Diagnostic_Tests|$))',
#         'Diagnostic_Tests': r'Diagnostic_Tests[:\s]*(.*?)\s*(?=\b(Condition|$))',
#         'Condition': r'Condition[:\s]*(.*?)\s*(?=\b(Patient_Questions|$))',
#         'Patient_Questions': r'Patient_Questions[:\s]*(.*?)\s*(?=\b(Examiner_Questions|$))',
#         'Examiner_Questions': r'Examiner_Questions[:\s]*(.*?)\s*(?=\b(Treatment|$))',
#         'Treatment': r'Treatment[:\s]*(.*?)\s*(?=\b(Monitoring|$))',
#         'Monitoring': r'Monitoring[:\s]*(.*?)\s*(?=\b(Prognosis|$))',
#         'Prognosis': r'Prognosis[:\s]*(.*?)\s*(?=\b(Differential_Diagnoses|$))',
#         'Differential_Diagnoses': r'Differential_Diagnoses[:\s]*(.*?)\s*(?=\b(Filter_Specialties|$))',
#         'Filter_Specialties': r'Filter_Specialties[:\s]*(.*?)\s*(?=\b(Filter_Presenting_Complaints|$))',
#         'Filter_Presenting_Complaints': r'Filter_Presenting_Complaints[:\s]*(.*?)\s*(?=\b(Filter_Condition|$))',
#         'Filter_Condition': r'Filter_Condition[:\s]*(.*?)\s*(?=\b(Filter_Location|$))',
#         'Filter_Location': r'Filter_Location[:\s]*(.*?)\s*(?=\b(Filter_Scenario|$))',
#         'Filter_Scenario': r'Filter_Scenario[:\s]*(.*?)\s*(?=\b(Case_created_by|$))',
#         'Case_created_by': r'Case_created_by[:\s]*(.*?)\s*(?=\b(Reviewed_by_1|$))',
#         'Reviewed_by_1': r'Reviewed_by_1[:\s]*(.*?)\s*(?=\b(Reviewed_by_2|$))',
#         'Reviewed_by_2': r'Reviewed_by_2[:\s]*(.*?)\s*(?=\n|$)',  # End of document or section
#     }
#
#     # Remove unnecessary line breaks and tabs
#     cleaned_text = doc_text.replace('\n', ' ').replace('\t', ' ')
#
#     # Use regex to split the document into sections by Case Code
#     # case_sections = re.split(r'\bCase_Code:\s*\S+', cleaned_text)
#     case_sections = re.split(r'(?=\bCase_Code[:\s]*\S+)', cleaned_text)
#     print(case_sections)
#
#     cases = []
#     for section in case_sections[1:]:  # Skip the first section, as it will be empty before the first match
#         case_data = {}
#         case_code_match = re.search(patterns['Case_Code'], section, re.DOTALL | re.IGNORECASE)
#         if case_code_match:
#             case_data['Case_Code'] = case_code_match.group(1).strip()
#         else:
#             case_data['Case_Code'] = "Not Found"
#         for key, pattern in patterns.items():
#             if key == 'Case_Code':
#                 continue
#                 # Adjust the pattern to search within the current section
#             match = re.search(pattern, section, re.DOTALL | re.IGNORECASE)
#             if match:
#                 case_data[key] = match.group(1).strip()
#             else:
#                 case_data[key] = "Not Found"
#         cases.append(case_data)
#
#     return cases