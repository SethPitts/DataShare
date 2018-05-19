
    LIBNAME ndbmeta "Data";

/* Create Data Dict for 0054
*/

/* Create the intitial DD by filtering by protocol and object type to remove HIDDEN fields
*/
data ndbmeta.data_dict_0054_1;
	set ndbmeta.meta;
	if substr(PROTSEG,1,4) eq '0054' AND OBJTYPE ne 'HIDDEN';
	SEGMENT = substr(PROTSEG,5,1);
	keep PROTSEG SEGMENT SCREENID SCREENNAME FIELD_NAME FIELD_TYPE FIELD_LEN CODELIST KEYFIELD NLOW NHIGH SKIPCOND RENDER READONLY SEQ OBJTYPE QTEXT;
run;
/* sort DD and remove duplicates
*/

proc sort data=ndbmeta.data_dict_0054_1; by PROTSEG SCREENID SEQ FIELD_NAME; run;

data ndbmeta.data_dict_0054_final;
	set ndbmeta.data_dict_0054_1;
	drop SEGMENT SEQ;
run;

proc export data=ndbmeta.data_dict_0054_final
	outfile='Data\DataDictionary_raw.csv'
	dbms=csv
	replace;
run;

/* Create list of screens in the DD
*/

data ndbmeta.screens;
	set ndbmeta.data_dict_0054_final;
	keep SCREENID;
run;

proc sort data=ndbmeta.screens nodups; by SCREENID; run;
proc export data=ndbmeta.screens
	outfile='Data\screens.csv'
	dbms=csv
	replace;
run;

data ndbmeta.all_segments;
	set ndbmeta.data_dict_0054_1;
	keep SEGMENT;
run;

proc sort data=ndbmeta.all_segments nodups; by SEGMENT; run;
proc export data=ndbmeta.all_segments
	outfile='Data\segments.csv'
	dbms=csv
	replace;
run;

