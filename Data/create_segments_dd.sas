
    LIBNAME ndbmeta "Data";

/* Create Data Dict for 0054
*/

/* Create the intitial DD by filtering by protocol and object type to remove HIDDEN fields
*/


data ndbmeta.data_dict_0054_segment_A;
    set ndbmeta.data_dict_0054_1;
    if SEGMENT = 'A';
    drop SEGMENT;
run;

proc sort data=ndbmeta.data_dict_0054_segment_A; by SCREENID SEQ FIELD_NAME;
proc export data=ndbmeta.data_dict_0054_segment_A
    outfile='Data\DataDict_Segment_A.csv'
    dbms=csv
    replace;
run;
data ndbmeta.data_dict_0054_segment_B;
    set ndbmeta.data_dict_0054_1;
    if SEGMENT = 'B';
    drop SEGMENT;
run;

proc sort data=ndbmeta.data_dict_0054_segment_B; by SCREENID SEQ FIELD_NAME;
proc export data=ndbmeta.data_dict_0054_segment_B
    outfile='Data\DataDict_Segment_B.csv'
    dbms=csv
    replace;
run;
data ndbmeta.data_dict_0054_segment_Z;
    set ndbmeta.data_dict_0054_1;
    if SEGMENT = 'Z';
    drop SEGMENT;
run;

proc sort data=ndbmeta.data_dict_0054_segment_Z; by SCREENID SEQ FIELD_NAME;
proc export data=ndbmeta.data_dict_0054_segment_Z
    outfile='Data\DataDict_Segment_Z.csv'
    dbms=csv
    replace;
run;