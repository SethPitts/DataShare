
/* QC program for 0054 data share */
ods html close;
        
%let input = G:\NIDADSC\spitts\Python_Projects\Data_Share\0054;
libname in "&input";
       
        
*Get formats;
        
options fmtsearch=(work input);
        
ods rtf file="G:\NIDADSC\spitts\Python_Projects\Data_Share\0054\QC\QC_&SYSDATE..rtf";

proc contents data=in.AD1 varnum; title 'AD1'; run;
proc contents data=in.AD2 varnum; title 'AD2'; run;
proc contents data=in.AD3 varnum; title 'AD3'; run;
proc contents data=in.ASU varnum; title 'ASU'; run;
proc contents data=in.BBL varnum; title 'BBL'; run;
proc contents data=in.CHP varnum; title 'CHP'; run;
proc contents data=in.D54 varnum; title 'D54'; run;
proc contents data=in.DSM varnum; title 'DSM'; run;
proc contents data=in.EC0054A varnum; title 'EC0054A'; run;
proc contents data=in.EC0054B varnum; title 'EC0054B'; run;
proc contents data=in.EC0054Z varnum; title 'EC0054Z'; run;
proc contents data=in.ECG varnum; title 'ECG'; run;
proc contents data=in.enroll varnum; title 'enroll'; run;
proc contents data=in.EOM varnum; title 'EOM'; run;
proc contents data=in.ER0054A varnum; title 'ER0054A'; run;
proc contents data=in.ER0054B varnum; title 'ER0054B'; run;
proc contents data=in.ER0054Z varnum; title 'ER0054Z'; run;
proc contents data=in.HIV varnum; title 'HIV'; run;
proc contents data=in.INA varnum; title 'INA'; run;
proc contents data=in.INJ varnum; title 'INJ'; run;
proc contents data=in.INV varnum; title 'INV'; run;
proc contents data=in.INX varnum; title 'INX'; run;
proc contents data=in.LAB varnum; title 'LAB'; run;
proc contents data=in.MHX varnum; title 'MHX'; run;
proc contents data=in.MVF varnum; title 'MVF'; run;
proc contents data=in.NXC varnum; title 'NXC'; run;
proc contents data=in.PBC varnum; title 'PBC'; run;
proc contents data=in.PCM varnum; title 'PCM'; run;
proc contents data=in.PDR varnum; title 'PDR'; run;
proc contents data=in.PDV varnum; title 'PDV'; run;
proc contents data=in.PEX varnum; title 'PEX'; run;
proc contents data=in.PO1 varnum; title 'PO1'; run;
proc contents data=in.PO2 varnum; title 'PO2'; run;
proc contents data=in.PO3 varnum; title 'PO3'; run;
proc contents data=in.PO4 varnum; title 'PO4'; run;
proc contents data=in.PRG varnum; title 'PRG'; run;
proc contents data=in.PSF varnum; title 'PSF'; run;
proc contents data=in.PXS varnum; title 'PXS'; run;
proc contents data=in.QLP varnum; title 'QLP'; run;
proc contents data=in.RXS varnum; title 'RXS'; run;
proc contents data=in.STT varnum; title 'STT'; run;
proc contents data=in.T54 varnum; title 'T54'; run;
proc contents data=in.TAP varnum; title 'TAP'; run;
proc contents data=in.TEA varnum; title 'TEA'; run;
proc contents data=in.TUH varnum; title 'TUH'; run;
proc contents data=in.UDC varnum; title 'UDC'; run;
proc contents data=in.UDE varnum; title 'UDE'; run;
proc contents data=in.UDS varnum; title 'UDS'; run;
proc contents data=in.VAS varnum; title 'VAS'; run;
proc contents data=in.VIS varnum; title 'VIS'; run;

ods rtf close;