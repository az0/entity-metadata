/*
Purpose: ETL parsing errors from the Physician data set

Copyright (C) 2017 by Andrew Ziem.  All rights reserved.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

*/

%let a=%sysget(SAS_EXECFILEPATH);
%let b=%sysget(SAS_EXECFILENAME);
%let mv_code_dir = %sysfunc(tranwrd(&a,&b,));
%put &=mv_code_dir;
%let mv_data_dir = &mv_code_dir.../data;
%put &=mv_data_dir;

proc import
	datafile="&mv_data_dir.\cms-physician-permutation-tagged.csv"
	out=tagged
	dbms=csv
	replace;
run;

proc freq data=tagged;
	table error_any;
run;

proc freq data=tagged;
	table tag_type*error_any/nocol nopercent;
run;

data tagged2;
	set tagged;
	if error_any eq 'True';
run;

proc surveyselect
	data=tagged2
	method=srs
	n=1000
	out=sample
	noprint;
run;

proc export
	data=sample
	outfile="&mv_data_dir./cms-physician-errors-sample.csv"
	dbms=csv
	replace;
run;
