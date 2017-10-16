/*

Purpose: ETL data for use with probablepeople library
Input data set: wikidata-church.csv
Data source: Wikidata via wikidata_org.py

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

/* import */
filename incsv "&mv_data_dir./wikidata-church.csv" encoding="utf-8" lrecl=32767;

proc import
	datafile=incsv
	out=church1
	dbms=csv
	replace;
run;

/* count instance types */
proc freq data=church1 order=freq;
	table instance_of;
run;

/* subset */
data church2;
	set church1;
	/* church (not human, building, cemetary, etc.) */
	if instance_of in ('church', 'cathedral', 'chapel','abbey');
	if not prxmatch('/\b(school|cemetery)\b/io', name);
	/* comma or parenthesis often signifies a location */
	if not prxmatch('/[(),]/o', name);
run;

/* browse */
proc sort data=church2;
	by instance_of name;
run;

/* remove duplicates */
proc sort data=church2 nodupkey;
	by name;
run;

/* export */
filename outcsv "&mv_data_dir./wikidata-church-filtered.csv" encoding="utf-8" lrecl=32767;

proc export
	outfile=outcsv
	data=church2(keep=name)
	dbms=csv
	replace;
run;
