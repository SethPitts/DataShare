import subprocess
import os
from create_qc_sas_file import create_dd_sas_file, create_qc_sas_file, create_text_fields_file,\
    create_dd_by_segment_file
DATA_FOLDER_PATH = r"G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\Data"


def create_data_share():
    # create the protocol data dict
    sas_location = r'S:\SAS 9.4\x86\SASFoundation\9.4\sas.exe'
    dd_sas_file = os.path.join(DATA_FOLDER_PATH, 'create_dd.sas')
    qc_sas_file = os.path.join(DATA_FOLDER_PATH, 'create_qc_file.sas')
    find_free_text_fields_sas_file = os.path.join(DATA_FOLDER_PATH, 'find_free_text_fields.sas')
    segment_dd_file = os.path.join(DATA_FOLDER_PATH, 'create_segments_dd.sas')

    # Create the DD
    create_dd_sas_file()
    subprocess.call([sas_location, dd_sas_file])
    create_qc_sas_file()
    subprocess.call([sas_location, qc_sas_file])
    create_text_fields_file()
    subprocess.call([sas_location, find_free_text_fields_sas_file])
    create_dd_by_segment_file()
    subprocess.call([sas_location, segment_dd_file])


def main():
    create_data_share()


if __name__ == '__main__':
    main()
