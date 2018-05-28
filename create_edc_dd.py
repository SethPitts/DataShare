import pandas as pd
import os


def create_edc_dd_sas_file(edc_sas_file_path, edc_forms_file_path):
    edc_data_libname_path = ""
    sas_file_directory = os.path.dirname(edc_sas_file_path)

    with open(edc_forms_file_path, 'r') as edc_file, open(edc_sas_file_path, 'w', newline="\n") as sas_file:
        # LIBNAME statement
        sas_file.write('LIBNAME edc "{}";\n\n'.format(edc_data_libname_path))

        # create a data frame from the edc file
        edc_data_frame = pd.read_csv(edc_file)

        #  Create a dataset for each form in the edc file. Keep only the variables we want for the Data Dictionary
        #  And sort the data set by PROTSEG SCREENID FIELD_NAME keep only the fields you want in the Data Dict
        keep_variables = \
            "PROTSEG SCREENID FIELD_NAME SCREENNAME KEYFIELD FIELD_TYPE FIELD_LEN CODELIST NLOW NHIGH SLOW SHIGH SKIPCOND RENDER"
        sort_variables = \
            "SCREENID SCREENNAME KEYFIELD FIELD_NAME FIELD_TYPE FIELD_LEN CODELIST NLOW NHIGH SLOW SHIGH SKIPCOND RENDER"
        create_dataset_template = \
            'data {dataset};\n\tset edc.meta;\n\tif SCREENID = "{dataset}";\n\tkeep {keep_variables};\nrun;\n\n'
        sort_dataset_template = "proc sort data = {dataset} nodupkey;\n\tby {sort_variables};\nrun;\n\n"
        forms_data_frame = edc_data_frame.SCREENID
        forms_in_edc = []
        for form in forms_data_frame:
            forms_in_edc.append(form)
            dataset_info = {'dataset': form,
                            'keep_variables': keep_variables,
                            'sort_variables': sort_variables
                            }
            sas_file.write(create_dataset_template.format(**dataset_info))
            sas_file.write(sort_dataset_template.format(**dataset_info))

        # merge all the datasets by all the fields in the Data Dictionary other than protseg to remove duplicates
        # but keep fields that have different rendering conditions
        merge_variables = sort_variables
        edc_form_data = {'forms_in_edc': " ".join(forms_in_edc),
                         'merge_variables': merge_variables
                         }

        # merged dataset should already be sorted
        merged_dataset_string = \
            'data edc_dd;\n\tmerge {forms_in_edc};\n\tby {merge_variables};\n\tif substr(PROTSEG,1,4) = "0054";\nrun;\n\n'.format(
                **edc_form_data)
        sas_file.write(merged_dataset_string)

        # export the dataset to csv
        # $ TODO: Use ODS to write to excel
        edc_csv_path = os.path.join(sas_file_directory, 'edc_dd.csv')
        export_string = 'proc export data=edc_dd\n\toutfile="{edc_csv_path}"\n\tdbms=csv\n\treplace;\nrun;'.format(
            edc_csv_path=edc_csv_path)
        sas_file.write(export_string)
        print("wrote sas file to {}".format(edc_sas_file_path))


def main():
    edc_forms_file_path = r"/home/beliefs22/PycharmProjects/DataShare/QC/edc_forms.csv"
    edc_sas_file_path = os.path.join(os.path.dirname(edc_forms_file_path), 'create_edc_dd.sas')

    create_edc_dd_sas_file(edc_sas_file_path, edc_forms_file_path)


if __name__ == '__main__':
    main()
