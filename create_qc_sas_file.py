import csv
import os

PROTOCOL = '0054'
DATA_SHARE_PATHWAY = r"G:\NIDADSC\spitts\Python_Projects\Data_Share\0054"
QC_FOLDER_PATHWAY = r"G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\QC"
DOCUMENT_FOLDER_PATHWAY = r"G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\Documents"
DATA_FOLDER_PATH = r"G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\Data"


def create_dd_sas_file():
    dd_sas_files_path = os.path.join(DATA_FOLDER_PATH, 'create_dd.sas')
    template = r"""
    LIBNAME ndbmeta "{}";

/* Create Data Dict for {}
*/

/* Create the intitial DD by filtering by protocol and object type to remove HIDDEN fields
*/
data ndbmeta.data_dict_{}_1;
	set ndbmeta.meta;
	if substr(PROTSEG,1,4) eq '{}' AND OBJTYPE ne 'HIDDEN';
	SEGMENT = substr(PROTSEG,5,1);
	keep PROTSEG SEGMENT SCREENID SCREENNAME FIELD_NAME FIELD_TYPE FIELD_LEN CODELIST KEYFIELD NLOW NHIGH SKIPCOND RENDER READONLY SEQ OBJTYPE QTEXT;
run;
/* sort DD and remove duplicates
*/

proc sort data=ndbmeta.data_dict_{}_1; by PROTSEG SCREENID SEQ FIELD_NAME; run;

data ndbmeta.data_dict_{}_final;
	set ndbmeta.data_dict_{}_1;
	drop SEGMENT SEQ;
run;

proc export data=ndbmeta.data_dict_{}_final
	outfile='{}\DataDictionary_raw.csv'
	dbms=csv
	replace;
run;

/* Create list of screens in the DD
*/

data ndbmeta.screens;
	set ndbmeta.data_dict_{}_final;
	keep SCREENID;
run;

proc sort data=ndbmeta.screens nodups; by SCREENID; run;
proc export data=ndbmeta.screens
	outfile='{}\screens.csv'
	dbms=csv
	replace;
run;

data ndbmeta.all_segments;
	set ndbmeta.data_dict_{}_1;
	keep SEGMENT;
run;

proc sort data=ndbmeta.all_segments nodups; by SEGMENT; run;
proc export data=ndbmeta.all_segments
	outfile='{}\segments.csv'
	dbms=csv
	replace;
run;
""".format(DATA_FOLDER_PATH, PROTOCOL, PROTOCOL, PROTOCOL, PROTOCOL, PROTOCOL,
           PROTOCOL,PROTOCOL, DOCUMENT_FOLDER_PATHWAY, PROTOCOL, DATA_FOLDER_PATH, PROTOCOL, DATA_FOLDER_PATH)

    print(template, file=open(dd_sas_files_path, 'w'))


def create_qc_sas_file():
    # Get Screens
    screen_file = os.path.join(DATA_FOLDER_PATH, 'screens.csv')
    segments_file = os.path.join(DATA_FOLDER_PATH, 'segments.csv')
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
/* QC program for {} data share */
ods html close;
        
%let input = {};
libname in "&input";
       
        
*Get formats;
        
options fmtsearch=(work input);
        
ods rtf file="{}\QC_&SYSDATE..rtf";""" + "\n"
        sas_file.write(base_template.format(PROTOCOL, DATA_FOLDER_PATH, QC_FOLDER_PATHWAY) + "\n")

        enr_table_templates = ['ER{}{}', 'EC{}{}']
        enr_tables = []
        for segment in segments:
            for template in enr_table_templates:
                enr_tables.append(template.format(PROTOCOL, segment))
        screens += enr_tables
        screens.remove('ENR')
        screens.append('enroll')
        proc_contents_template = r"""proc contents data=in.{} varnum; title '{}'; run;"""
        screens.sort(key=lambda x: x.lower())
        for screen in screens:
            sas_file.write(proc_contents_template.format(screen, screen) + "\n")

        sas_file.write('\nods rtf close;')


def create_dd_by_segment_file():
    segments_file = os.path.join(DATA_FOLDER_PATH, 'segments.csv')
    with open(segments_file, 'r') as segments_csv:
        segments = csv.reader(segments_csv)
        # skip headers
        next(segments)
        segments = [row[0] for row in segments]

    base_template = """
    LIBNAME ndbmeta "{}";

/* Create Data Dict for {}
*/

/* Create the intitial DD by filtering by protocol and object type to remove HIDDEN fields
*/""".format(DATA_FOLDER_PATH, PROTOCOL)

    data_template = """
data ndbmeta.data_dict_{}_segment_{};
    set ndbmeta.data_dict_{}_1;
    if SEGMENT = '{}';
    drop SEGMENT;
run;

proc sort data=ndbmeta.data_dict_{}_segment_{}; by SCREENID SEQ FIELD_NAME;
proc export data=ndbmeta.data_dict_{}_segment_{}
    outfile='{}\DataDict_Segment_{}.csv'
    dbms=csv
    replace;
run;"""

    with open(os.path.join(DATA_FOLDER_PATH, 'create_segments_dd.sas'), 'w') as sas_file:
        sas_file.write(base_template + "\n\n")
        for segment in segments:
            sas_file.write(data_template.format(PROTOCOL, segment, PROTOCOL, segment,
                                                PROTOCOL, segment, PROTOCOL, segment,
                                                DATA_FOLDER_PATH, segment))


def create_text_fields_file():
    text_fields_file_name = os.path.join(DATA_FOLDER_PATH, 'find_free_text_fields.sas')
    template = r"""
LIBNAME metadata "{}";

data filter_meta;
	set metadata.meta;
	if substr(PROTSEG,1,4) eq '{}' AND OBJTYPE ne 'HIDDEN' AND KEYFIELD = 0 AND ((FIELD_TYPE in ('C','M') AND FIELD_LEN gt 3) OR
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

ods rtf file="{}\deidentification_0054_raw.rtf";

proc report data=final split='|' headline center nowd;
	 columns ("The following variables are free text fields" AD1--VIS);
	 define AD1--VIS / display center;
run;
ods rtf close;
""".format(DATA_FOLDER_PATH, PROTOCOL, DOCUMENT_FOLDER_PATHWAY)

    with open(text_fields_file_name, 'w') as outfile:
        outfile.write(template)


def main():

    create_qc_sas_file()
    create_text_fields_file()
    create_dd_sas_file()


if __name__ == '__main__':
    main()
