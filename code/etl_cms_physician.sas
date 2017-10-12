/*

Purpose: ETL data for use with probablepeople library
Title:  Physician Compare National Downloadable File 
Publisher: Centers for Medicare & Medicaid Services
URL: https://www.healthdata.gov/dataset/physician-compare-national-downloadable-file
Size of input file: 2,249,045 rows; 625MB

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
proc import
	datafile="&mv_data_dir./input/cms-Physician_Compare_National_Downloadable_File.csv"
	out=ph
	dbms=csv;
run;

/* limit to persons (not the institution) */
data ph_person;
	/* reorder variables */

	retain npi first_name middle_name last_name suffix credential gender;
	/* lengthen */
	format credential $6.;
	set ph;
	
	/* Fix gender for one case (James) */
	if npi=1457496556 then gender='M';

	/*
Sometimes the suffix is in the last name field

Examples:
HYATT III
BILLMAN II
CAMMACK IV
ROGERS, JR
BARTON JR
GARZA  III
*/
	re_suffix = prxparse('/,?\s+(I|II|III|IV|V|VII|VIII|IX|X|JR\.?|SR\.?)$/o');
	if prxmatch(re_suffix, strip(last_name)) then do;
		suffix = prxposn(re_suffix, 1, strip(last_name));
		last_name = prxchange('s/,?\s+(I|II|III|IV|V|VII|VIII|IX|X|JR\.?|SR\.?)$//o', -1, strip(last_name));
		end;
	if suffix eq 'JR' then suffix = 'JR.';
	if suffix eq 'SR' then suffix = 'SR.';

	/* Remove extra spaces */
	first_name = strip(compbl(first_name));
	last_name = strip(compbl(last_name));

	keep npi last_name first_name middle_name suffix gender credential;
run;

/* remove duplicates */
proc sort data=ph_person nodupkey;
	by _all_;
run;

/* export */
proc export
	data=ph_person
	outfile="&mv_data_dir./cms-physician.csv"
	dbms=csv
	replace;
run;
	

/* from https://blogs.sas.com/content/iml/2015/10/05/random-integers-sas.html */
/* SAS macro that duplicates the Excel RANDBETWEEN function */
%macro RandBetween(min, max);
   (&min + floor((1+&max-&min)*rand("uniform")))
%mend;

/* create permutations for probablepeople */
data ph_person_permutation;
	set ph_person;

	/* set random seed */
	call streaminit(81649715);
	
	/* permutate prefix */
	format prefix $13.;
	if gender = 'M' then do;
		style_prefix = %RandBetween(0, 4);
		select (style_prefix);
			when (0) prefix='';
			when (1) prefix='Dr.';
			when (2) prefix='Mr.';
			when (3) prefix='Mr. & Mrs.';
			when (4) prefix='Dr. & Mrs.';
		end;
		end;
	else if gender='F' then do;
		style_prefix = %RandBetween(0, 4);
		select (style_prefix);
			when (0) prefix='';
			when (1) prefix='Dr.';
			when (2) prefix='Miss';
			when (3) prefix='Ms.';
			when (4) prefix='Mrs.';
		end;
		end;
	else abort cancel;

	/* focus on MD and DDS */
	if credential='MD' then credential='M.D.';
	else if credential='DDS' then credential='D.D.S.';
	else credential='';

	/* permutate presentation of credentials */
	/*
		0 = no credential
		2 = "John Smith, MD"
	*/
	style_credential = %RandBetween(0, 1);
	if missing(credential) then style_credential = 0;
	format use_credential $7.;
	use_credential = credential;
	select (style_credential);
			/* omit credential */
			when (0)
				do;
				
				use_credential = ' ';
				credential = ' ';
				end;
			/* prefix with comma (which may be removed in another step) */
			when (1) use_credential = ', '||use_credential;
		end;
	drop style_credential;

	/*
		Use comma with Jr. and Sr. but not numerals 
		https://style.mla.org/2016/08/23/names-with-suffixes/
	*/
	format use_suffix $5.;
	if suffix in ('JR.', 'SR.') then use_suffix = ', '||strip(suffix);
	else use_suffix = ' '||strip(suffix);

	name = catx(' ', prefix, first_name, middle_name, strip(last_name)||use_suffix||strip(use_credential));
	
	/* permutate use of commas */
	style_comma = %RandBetween(0, 1);
	if style_comma eq 1 then name = compress(name, ',');

	/* permutate use of periods (prefix, middle name, suffix, and credentials) */
	style_period = %RandBetween(0, 1);
	if style_period eq 1 then name = compress(name, '.');

	/* permutate between ampersand and word "and" */
	style_and = %RandBetween(0, 1);
	if style_and eq 1 then name = tranwrd(name, '&', 'and');

	/* remove double spaces */
	name = compbl(name);
	
	/* remove space before comma */
	name = tranwrd(name, ' ,', ',');

	/* ununeded variables */
	drop npi gender use_: style_:;
run;

/* export */
proc export
	data=ph_person_permutation
	outfile="&mv_data_dir./cms-physician-permutation.csv"
	dbms=csv
	replace;
run;
