import pandas as pd
from collections import defaultdict
import csv


def find_text_fields(data_dictionary_pathway):
    # Create data frame using columns 0,1,4,5 and 6 of excel file, skipping first 7 rows so the file has headers
    data_dictionary_df = pd.read_excel(data_dictionary_pathway, skiprows=7, usecols=[0, 1, 4, 5, 6])
    data_dictionary_df.to_csv('{}_for_sas.csv'.format(data_dictionary_pathway))
    # Create data from from meta data sas table
    meta_data_df = pd.read_sas('meta.sas7bdat',format='sas7bdat')

    # Create list of variables in data dictionary
    data_dictionary_variables = defaultdict(dict)
    for i in range(len(data_dictionary_df)):
        key_field = data_dictionary_df.ix[i]['Key Field']
        field_name = data_dictionary_df.ix[i]['Field Name']
        field_type = data_dictionary_df.ix[i]['Type']
        field_length = data_dictionary_df.ix[i]['Length and Decimals']
        field_object_type = data_dictionary_df.ix[i]['Object Type']

        data_dictionary_variables[field_name] = {'key_field': key_field,
                                                 'field_type': field_type,
                                                 'field_length': field_length,
                                                 'field_object_type': field_object_type
                                                 }
    # Add Screen name to the variable information
    for i in range(len(meta_data_df)):
        field_name = meta_data_df.ix[i]['FIELD_NAME'].decode("utf-8")
        screen_id = meta_data_df.ix[i]['SCREENID'].decode("utf-8")
        if data_dictionary_variables.get(field_name):
            data_dictionary_variables[field_name]['SCREENID'] = screen_id

    # Parse through excel file
    text_fields = []
    de_identification_document_info = defaultdict(list)
    for field, field_info in data_dictionary_variables.items():
        key_field = field_info['key_field']
        field_length = field_info['field_length']
        field_type = field_info['field_type']
        field_object_type = field_info['field_object_type']
        if field_info.get('SCREENID') is None:
            screen_id = 'NONE'
        else:
            screen_id = field_info['SCREENID']
        if (key_field != '*' and field_type in ('C', 'M')) and (field_length > 3 or
                                                                (field_length <= 3 and field_object_type == 'TEXTBOX')):
            if type(field) == str and field != 'Field Name':
                text_fields.append([field ,screen_id])
                # if field not in de_identification_document_info[screen_id]:
                #     de_identification_document_info[screen_id].append(field)
    # Create CSV from found fields
    csv_writer = csv.writer(open('Free_Text_Variables.csv', 'w', newline=""))
    # Write headers
    csv_writer.writerow(['Field_Name', 'Table'])
    csv_writer.writerows(text_fields)
    # # Clear document - this is the dumb way to do this
    # print("", file=open('text_entry_fields.txt.', 'w'))
    # for text_field in text_fields:
    #     print(text_field, file=open('{}.txt'.format(data_dictionary_pathway), 'a'))
    #
    # de_identification_document_info_df = pd.DataFrame.from_dict(de_identification_document_info)
    # # excel_writer = pd.ExcelWriter('{}_Deidentification.xlsx'.format(data_dictionary_pathway))
    #
    # de_identification_document_info_df.to_csv('{}.csv'.format(data_dictionary_pathway))
    #
    # # excel_writer.save()


def main():
    data_dictionary_pathway = 'DataDictionary_updated_02MAY.xlsx'
    find_text_fields(data_dictionary_pathway)


if __name__ == '__main__':
    main()
