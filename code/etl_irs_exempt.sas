/* 
Summary:		ETL the exempt organizations business master file
By: 			Compassion International, November 2019
Data source: 	https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf

*/

%let mv_input_dir = /some/input/folder/;
%let mv_output_dir = /some/input/folder/;

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
	set irs:(keep=name group status state zip subsection affiliation classification activity ruling ntee_cd ded:);
run;

proc export
	data=irs
	outfile="&mv_output_dir/irs_exempt.csv"
	dbms=csv
	replace;
quit;
