import pandas as pd
import csv

# Parse through text document to find lines that start with numbers. These lines contain variables names
with open(r'G:\NIDADSC\DATA_SHARE\CTN0054\QC\QC_11MAY18.txt', 'r') as data_share_file:
    qc_file_variables = []
    for line in data_share_file:
        if line:
            line = line.strip().split()
            if line:
                if line[0].isnumeric():
                    qc_file_variables.append(line[1])

# Create DF using first 2 columns of original data dictionary excel file, skipping first 7 rows so the file has headers
modified_data_dictionary_variables = []
data_dictionary_df = pd.read_excel(r'G:\NIDADSC\DATA_SHARE\CTN0054\Documents\DataDictionary_updated_02MAY.xlsx',
                                   skiprows=7, usecols=1)
for j in range(len(data_dictionary_df)):
    field_name = data_dictionary_df.ix[j]['Field Name']
    if type(field_name) == str and field_name != 'Field Name':
        modified_data_dictionary_variables.append(field_name)

missing_qc_file_variables = qc_file_variables[:]
missing_modified_data_dictionary_variables = modified_data_dictionary_variables[:]

# TODO: remove found data from each list so that the remaining items are the ones without matches

# In the data share but not in the data dict
for variable in qc_file_variables:
    if variable in modified_data_dictionary_variables:
        missing_qc_file_variables.remove(variable)


# In the data dict but not in the data share
for variable in modified_data_dictionary_variables:
    if variable in qc_file_variables:
        missing_modified_data_dictionary_variables.remove(variable)

missing_qc_file_variables = [variable
                             for variable in missing_qc_file_variables
                             if variable not in ("SITE", "PROT", "PROJID", "RANDDT",  "PATID")
                             ]

missing_modified_data_dictionary_variables = [variable
                                              for variable in missing_modified_data_dictionary_variables
                                              if variable not in ("SITE", "PROT", "PROJID", "RANDDT",  "PATID")
                                              ]

headers = ['Field', 'QC_Comments', 'Review_Comments']
with open("Fields_Missing_From_QC_File.csv", 'w', newline="\n") as missing_qc_file:
    csv_writer = csv.writer(missing_qc_file)
    csv_writer.writerow(headers)
    for row in missing_modified_data_dictionary_variables:
        csv_writer.writerow([row])

with open("Fields_Missing_From_Modified_DD.csv", 'w', newline="\n") as missing_dd_file:
    csv_writer = csv.writer(missing_dd_file)
    csv_writer.writerow(headers)
    for row in missing_qc_file_variables:
        csv_writer.writerow([row])
