/* dump coefficient files to csv and sas7bdat */

filename inc "/folders/myfolders/sasuser.v94/cms_hcc_binary/C1209J2Y";
libname incoef "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport data=incoef.C1209J2Y infile=inc;
run;
proc export data=incoef.C1209J2Y
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/C1209J2Y.csv"
dbms=csv
replace;
run;

filename inc "/folders/myfolders/sasuser.v94/cms_hcc_binary/C2110H2R";
libname incoef "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport data=incoef.C2110H2R infile=inc;
run;
proc export data=incoef.C2110H2R
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/C2110H2R.csv"
dbms=csv
replace;
run;

filename inc "/folders/myfolders/sasuser.v94/cms_hcc_binary/C2214O5P";
libname incoef "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport data=incoef.C2214O5P infile=inc;
run;
proc export data=incoef.C2214O5P
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/C2214O5P.csv"
dbms=csv
replace;
run;

filename inc "/folders/myfolders/sasuser.v94/cms_hcc_binary/C2211L4P";
libname incoef "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport data=incoef.C2211L4P infile=inc;
run;
proc export data=incoef.C2211L4P
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/C2211L4P.csv"
dbms=csv
replace;
run;

/* dump format files to csv and sas7bdat */

filename inf "/folders/myfolders/sasuser.v94/cms_hcc_binary/F211690R";
libname cmshccfm "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport library=cmshccfm infile=inf;
run;
proc format lib=cmshccfm.formats cntlout=cmshccfm.F211690R;
select a-zzzzzzzz  $a-$zzzzzzzz;
run;
proc export data=cmshccfm.F211690R
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/F211690R.csv"
dbms=csv
replace;
run;

filename inf "/folders/myfolders/sasuser.v94/cms_hcc_binary/F2113J1R";
libname cmshccfm "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport library=cmshccfm infile=inf;
run;
proc format lib=cmshccfm.formats cntlout=cmshccfm.F2113J1R;
select a-zzzzzzzz  $a-$zzzzzzzz;
run;
proc export data=cmshccfm.F2113J1R
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/F2113J1R.csv"
dbms=csv
replace;
run;

filename inf "/folders/myfolders/sasuser.v94/cms_hcc_binary/F221690P";
libname cmshccfm "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport library=cmshccfm infile=inf;
run;
proc format lib=cmshccfm.formats cntlout=cmshccfm.F221690P;
select a-zzzzzzzz  $a-$zzzzzzzz;
run;
proc export data=cmshccfm.F221690P
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/F221690P.csv"
dbms=csv
replace;
run;

filename inf "/folders/myfolders/sasuser.v94/cms_hcc_binary/F2213L2P";
libname cmshccfm "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport library=cmshccfm infile=inf;
run;
proc format lib=cmshccfm.formats cntlout=cmshccfm.F2213L2P;
select a-zzzzzzzz  $a-$zzzzzzzz;
run;
proc export data=cmshccfm.F2213L2P
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/F2213L2P.csv"
dbms=csv
replace;
run;

filename inf "/folders/myfolders/sasuser.v94/cms_hcc_binary/F2117H1R";
libname cmshccfm "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport library=cmshccfm infile=inf;
run;
proc format lib=cmshccfm.formats cntlout=cmshccfm.F2117H1R;
select a-zzzzzzzz  $a-$zzzzzzzz;
run;
proc export data=cmshccfm.F2117H1R
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/F2117H1R.csv"
dbms=csv
replace;
run;

filename inf "/folders/myfolders/sasuser.v94/cms_hcc_binary/F1213H1Y";
libname cmshccfm "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport library=cmshccfm infile=inf;
run;
proc format lib=cmshccfm.formats cntlout=cmshccfm.F1213H1Y;
select a-zzzzzzzz  $a-$zzzzzzzz;
run;
proc export data=cmshccfm.F1213H1Y
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/F1213H1Y.csv"
dbms=csv
replace;
run;

filename inf "/folders/myfolders/sasuser.v94/cms_hcc_binary/F2217O1P";
libname cmshccfm "/folders/myfolders/sasuser.v94/cms_hcc_binary";
proc cimport library=cmshccfm infile=inf;
run;
proc format lib=cmshccfm.formats cntlout=cmshccfm.F2217O1P;
select a-zzzzzzzz  $a-$zzzzzzzz;
run;
proc export data=cmshccfm.F2217O1P
outfile="/folders/myfolders/sasuser.v94/cms_hcc_binary/F2217O1P.csv"
dbms=csv
replace;
run;

