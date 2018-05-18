LIBNAME ndbmeta "G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\Data";

/* Create Data Dict for 0054
*/

/* Create the intitial DD by filtering by protocol and object type to remove HIDDEN fields
*/
data data_dict_0054_1;
	set ndbmeta.meta;
	if substr(PROTSEG,1,4) eq '0054' AND OBJTYPE ne 'HIDDEN';
	SEGMENT = substr(PROTSEG, 5,1);
	keep SCREENID SEGMENT SCREENNAME FIELD_NAME FIELD_TYPE FIELD_LEN CODELIST KEYFIELD NLOW NHIGH SKIPCOND RENDER READONLY SEQ OBJTYPE QTEXT;
run;
/* sort DD and remove duplicates
*/

proc sort data=data_dict_0054_1 nodups; by SCREENID SEQ FIELD_NAME SKIPCOND RENDER; run;

data data_dict_0054_final;
	set data_dict_0054_1;
	drop SEQ;
run;

/* Create list of screens in the DD
*/

data screens;
	set data_dict_0054_final;
	keep SCREENID;
run;

proc sort data=screens nodups; by SCREENID; run;
proc export data=screens
	outfile='G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\screens.csv'
	dbms=csv
	replace;
run;

data all_segments;
	set data_dict_0054_1;
	keep SEGMENT;
run;

proc sort data=all_segments nodups; by SEGMENT; run;
proc export data=all_segments
	outfile='G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\segments.csv'
	dbms=csv
	replace;
run;
