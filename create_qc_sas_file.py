import csv
import os


def get_data_share_info():
    """
    Gets the pathway info for the current data share
    :return: dict containing the data share path info
    """
    PROTOCOL = input('What is the Protocol? ')
    DATA_SHARE_PATHWAY = input("WHat is the data share folder pathway? ")
    QC_FOLDER_PATHWAY = "QC"
    DOCUMENT_FOLDER_PATHWAY = "Documents"
    DATA_FOLDER_PATH = "Data"
    DATA_SHARE_INFO = {'PROTOCOL': PROTOCOL,
                       'DATA_SHARE_PATHWAY': DATA_SHARE_PATHWAY,
                       'QC_FOLDER_PATHWAY': QC_FOLDER_PATHWAY,
                       'DOCUMENT_FOLDER_PATHWAY': DOCUMENT_FOLDER_PATHWAY,
                       'DATA_FOLDER_PATH': DATA_FOLDER_PATH
                       }
    return DATA_SHARE_INFO


def create_dd_sas_file(DATA_SHARE_INFO):
    """
    Creates the sas file to create the data dictionary for the PROTOCOL
    :return: No return
    """
    dd_sas_files_path = os.path.join(DATA_SHARE_INFO['DATA_FOLDER_PATH'], 'create_dd.sas')
    sas_file_template = r"""
    LIBNAME ndbmeta "{DATA_FOLDER_PATH}";

/* Create Data Dict for {PROTOCOL}
*/

/* Create the intitial DD by filtering by protocol and object type to remove HIDDEN fields
*/
data ndbmeta.data_dict_{PROTOCOL}_1;
	set ndbmeta.meta;
	if substr(PROTSEG,1,4) eq '{PROTOCOL}' AND OBJTYPE ne 'HIDDEN';
	SEGMENT = substr(PROTSEG,5,1);
	keep PROTSEG SEGMENT SCREENID SCREENNAME FIELD_NAME FIELD_TYPE FIELD_LEN CODELIST KEYFIELD NLOW NHIGH SKIPCOND RENDER READONLY SEQ OBJTYPE QTEXT;
run;
/* sort DD and remove duplicates
*/

proc sort data=ndbmeta.data_dict_{PROTOCOL}_1; by PROTSEG SCREENID SEQ FIELD_NAME; run;

data ndbmeta.data_dict_{PROTOCOL}_final;
	set ndbmeta.data_dict_{PROTOCOL}_1;
	drop SEGMENT SEQ;
run;

proc export data=ndbmeta.data_dict_{PROTOCOL}_final
	outfile='{DATA_FOLDER_PATH}\DataDictionary_raw.csv'
	dbms=csv
	replace;
run;

/* Create list of screens in the DD
*/

data ndbmeta.screens;
	set ndbmeta.data_dict_{PROTOCOL}_final;
	keep SCREENID;
run;

proc sort data=ndbmeta.screens nodups; by SCREENID; run;
proc export data=ndbmeta.screens
	outfile='{DATA_FOLDER_PATH}\screens.csv'
	dbms=csv
	replace;
run;

data ndbmeta.all_segments;
	set ndbmeta.data_dict_{PROTOCOL}_1;
	keep SEGMENT;
run;

proc sort data=ndbmeta.all_segments nodups; by SEGMENT; run;
proc export data=ndbmeta.all_segments
	outfile='{DATA_FOLDER_PATH}\segments.csv'
	dbms=csv
	replace;
run;
""".format(**DATA_SHARE_INFO)

    print(sas_file_template, file=open(dd_sas_files_path, 'w'))


def create_qc_sas_file(DATA_SHARE_INFO):
    """
    Create QC sas file
    :return:
    """
    # Get Screens
    DATA_FOLDER_PATH = DATA_SHARE_INFO['DATA_FOLDER_PATH']
    screen_file = os.path.join(DATA_FOLDER_PATH, 'screens.csv')  # ALl screens in the DD
    segments_file = os.path.join(DATA_FOLDER_PATH, 'segments.csv')  # ALl segments in the DD
    sas_file_name = os.path.join(DATA_FOLDER_PATH, 'create_qc_file.sas')
    with open(screen_file, 'r') as screen_csv, open(segments_file, 'r') as segments_csv, \
            open(sas_file_name, 'w', newline="\n") as sas_file:
        screens = csv.reader(screen_csv)
        # skip headers
        next(screens)
        screens = [row[0] for row in screens]
        segments = csv.reader(segments_csv)
        # skip headers
        next(segments)
        segments = [row[0] for row in segments]
        base_template = r"""
/* QC program for {PROTOCOL} data share */
ods html close;
        
%let input = {DATA_FOLDER_PATH};
libname in "&input";
       
        
*Get formats;
        
options fmtsearch=(work input);
        
ods rtf file="{QC_FOLDER_PATHWAY}\QC_&SYSDATE..rtf";""" + "\n"
        sas_file.write(base_template.format(**DATA_SHARE_INFO) + "\n")

        enr_table_templates = ['ER{}{}', 'EC{}{}']
        enr_tables = []
        for segment in segments:
            for template in enr_table_templates:
                enr_tables.append(template.format(DATA_SHARE_INFO['PROTOCOL'], segment))
        screens += enr_tables
        screens.remove('ENR')
        screens.append('enroll')
        screens.append('dem')
        proc_contents_template = r"""proc contents data=in.{} varnum; title '{}'; run;"""
        screens.sort(key=lambda x: x.lower())
        for screen in screens:
            sas_file.write(proc_contents_template.format(screen, screen) + "\n")

        sas_file.write('\nods rtf close;')


def create_dd_by_segment_file(DATA_SHARE_INFO):
    segments_file = os.path.join(DATA_SHARE_INFO['DATA_FOLDER_PATH'], 'segments.csv')
    with open(segments_file, 'r') as segments_csv:
        segments = csv.reader(segments_csv)
        # skip headers
        next(segments)
        segments = [row[0] for row in segments]

    base_template = """
    LIBNAME ndbmeta "{DATA_FOLDER_PATH}";

/* Create Data Dict for {PROTOCOL}
*/

/* Create the intitial DD by filtering by protocol and object type to remove HIDDEN fields
*/""".format(**DATA_SHARE_INFO)

    data_template = """
data ndbmeta.data_dict_{PROTOCOL}_segment_{SEGMENT};
    set ndbmeta.data_dict_{PROTOCOL}_1;
    if SEGMENT = '{SEGMENT}';
    drop SEGMENT;
run;

proc sort data=ndbmeta.data_dict_{PROTOCOL}_segment_{SEGMENT}; by SCREENID SEQ FIELD_NAME;
proc export data=ndbmeta.data_dict_{PROTOCOL}_segment_{SEGMENT}
    outfile='{DATA_FOLDER_PATH}\DataDict_Segment_{SEGMENT}.csv'
    dbms=csv
    replace;
run;"""

    with open(os.path.join(DATA_SHARE_INFO['DATA_FOLDER_PATH'], 'create_segments_dd.sas'), 'w') as sas_file:
        sas_file.write(base_template + "\n\n")

        for segment in segments:
            segment_info = {'PROTOCOL': DATA_SHARE_INFO['PROTOCOL'],
                            'SEGMENT': segment,
                            'DATA_FOLDER_PATH': DATA_SHARE_INFO['DATA_FOLDER_PATH']
                            }
            sas_file.write(data_template.format(**segment_info))


def create_text_fields_file(DATA_SHARE_INFO):
    text_fields_file_name = os.path.join(DATA_SHARE_INFO['DATA_FOLDER_PATH'], 'find_free_text_fields.sas')
    template = r"""
LIBNAME metadata "{DATA_FOLDER_PATH}";

data filter_meta;
	set metadata.meta;
	if substr(PROTSEG,1,4) eq '{PROTOCOL}' AND OBJTYPE ne 'HIDDEN' AND KEYFIELD = 0 AND ((FIELD_TYPE in ('C','M') AND FIELD_LEN gt 3) OR
	(FIELD_LEN le 3 and OBJTYPE eq 'TEXTBOX'));
run;

proc sort data=filter_meta; by PROTSEG SCREENID FIELD_NAME; run;

data final_meta;
	set filter_meta;
	keep SCREENID FIELD_NAME;
run;

proc sort data=final_meta nodups; by SCREENID FIELD_NAME; run;

proc transpose data=final_meta out=final0;
	by SCREENID;
	var FIELD_NAME;
run;

proc transpose data=final0 out=final;
	id SCREENID;
	var col1-col44;
run;

title "Information Sheet for De-identification";
footnote1 j=center "•	We recommend AD1.A1DESCPT not be dropped because it is the verbatim AE term used for MedDRA coding.";
footnote2 j=center "•	Two fields in one cell with a dash indicates an array of fields with the numeric portion of the field name incremented by one, starting with the first listed field name and ending with the second listed field name.";
footnote3 j=center "•	We recommend that date variables be replaced by days from informed consent (S1CNSTDT).";
footnote4 j=center "•	HIV.HITESTMO and HIV.HITESTYR denote the month and year (respectively) of a participant’s most recent HIV test.";

ods rtf file="{DOCUMENT_FOLDER_PATHWAY}\deidentification_{PROTOCOL}_raw.rtf";

proc report data=final split='|' headline center nowd;
	 columns ("The following variables are free text fields" AD1--VIS);
	 define AD1--VIS / display center;
run;
ods rtf close;
""".format(**DATA_SHARE_INFO)

    with open(text_fields_file_name, 'w') as outfile:
        outfile.write(template)


def main():
    DATA_SHARE_INFO = get_data_share_info()
    create_qc_sas_file(DATA_SHARE_INFO)
    create_text_fields_file(DATA_SHARE_INFO)
    create_dd_sas_file(DATA_SHARE_INFO)
    create_dd_by_segment_file(DATA_SHARE_INFO)


if __name__ == '__main__':
    main()
