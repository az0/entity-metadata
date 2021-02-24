/* 
Summary:		ETL the exempt organizations business master file
By: 			Compassion International, November 2019
Data source: 	https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf

*/

%let mv_input_dir = /some/input/folder/;
%let mv_output_dir = /some/input/folder/;

libname h "&mv_input_dir";

%macro irs(code);
proc import
	datafile="&mv_input_dir/eo&code..csv"
	out=irs&code.
	dbms=csv
	replace
	;
quit;
%mend;


%irs(_xx)
%irs(1)
%irs(2)
%irs(3)
%irs(4)
%irs(_pr)

proc sql;
	drop table irs;
quit;

data irs;
	set irs:(keep=
		ein name state zip group subsection affiliation classification ruling
		deductibility foundation activity organization status tax_period ntee_cd
		);
	activity_str = put(activity, z9.);
	activity1 = substr(activity_str, 1, 3);
	activity2 = substr(activity_str, 4, 3);
	activity3 = substr(activity_str, 7, 3);
	drop activity activity_str;
run;

proc export
	data=irs
	outfile="&mv_output_dir/irs_exempt.csv"
	dbms=csv
	replace;
quit;

data h.irs_exempt;
	set irs;
run;
