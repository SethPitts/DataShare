
LIBNAME metadata "G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\Data";

data filter_meta;
	set metadata.meta;
	if substr(PROTSEG,1,4) eq '0054' AND OBJTYPE ne 'HIDDEN' AND KEYFIELD = 0 AND ((FIELD_TYPE in ('C','M') AND FIELD_LEN gt 3) OR
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

ods rtf file="G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\Documents\deidentification_0054_raw.rtf";

proc report data=final split='|' headline center nowd;
	 columns ("The following variables are free text fields" AD1--VIS);
	 define AD1--VIS / display center;
run;
ods rtf close;
