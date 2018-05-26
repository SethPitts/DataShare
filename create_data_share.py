import os
import subprocess

from create_qc_sas_file import create_dd_sas_file, create_qc_sas_file, create_text_fields_file, \
    create_dd_by_segment_file, get_data_share_info


data_share_info = get_data_share_info()


def create_data_share():
    # create the protocol data dict
    data_folder_path = data_share_info['DATA_FOLDER_PATH']
    sas_location = r'S:\SAS 9.4\x86\SASFoundation\9.4\sas.exe'
    dd_sas_file = os.path.join(data_folder_path, 'create_dd.sas')
    qc_sas_file = os.path.join(data_folder_path, 'create_qc_file.sas')
    find_free_text_fields_sas_file = os.path.join(data_folder_path, 'find_free_text_fields.sas')
    segment_dd_file = os.path.join(data_folder_path, 'create_segments_dd.sas')

    # Create the DD
    create_dd_sas_file(data_share_info)
    subprocess.call([sas_location, dd_sas_file])
    create_qc_sas_file(data_share_info)
    subprocess.call([sas_location, qc_sas_file])
    create_text_fields_file(data_share_info)
    subprocess.call([sas_location, find_free_text_fields_sas_file])
    create_dd_by_segment_file(data_share_info)
    subprocess.call([sas_location, segment_dd_file])


def main():
    create_data_share()


if __name__ == '__main__':
    main()
