# Entity Metadata

This repository contains code and data about people and organizations.
Potential uses include training and evaluation data sets to:

* Classify names as a person, business, or church
* Capitalize names with the proper case such as _McGregory_ or _de la Cruz_
* Improve the [probablepeople](https://github.com/datamade/probablepeople) parser library
* [Generate names](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
* Classify race or ethnicity of person from name

# Data sets

| Entity  | Source | Download |
|-----------|----------------------------------------------------------|------------------------------------------------------------------------------|
| Physician | [CMS](https://data.cms.gov/provider-data/dataset/mj5m-pzi6) | [CSV](https://sourceforge.net/projects/entity-metadata/files/cms_physician/) |
| Author | [Open Library](https://openlibrary.org/developers/dumps) | [CSV](https://sourceforge.net/projects/entity-metadata/files/open_library/) |
| Academic author | [Open Academic Graph](https://www.aminer.org/oag2019) | [CSV](https://sourceforge.net/projects/entity-metadata/files/open_academic_graph/) |
| Person | Wikidata | [CSV](https://sourceforge.net/projects/entity-metadata/files/wikidata/person/)
| Person: Nicknames | onyxrev | [CSV](https://sourceforge.net/projects/entity-metadata/files/nicknames/)
| Voter | [Florida Voter Registration](https://dos.fl.gov/elections/data-statistics/voter-registration-statistics/voter-extract-request/) | [CSV](https://sourceforge.net/projects/entity-metadata/files/voter_registration/florida/)
| Voter | [North Carolina Voter Registration](https://www.ncsbe.gov/results-data/voter-registration-data) | [CSV](https://sourceforge.net/projects/entity-metadata/files/voter_registration/north_carolina/)
| Church | Wikidata via SPARQL | [CSV](https://sourceforge.net/projects/entity-metadata/files/wikidata/church/) |
| Licensee | US States | [CSV](https://sourceforge.net/projects/entity-metadata/files/license_roster/) |
| Inmate | Florida | [CSV](https://sourceforge.net/projects/entity-metadata/files/offender/) |
| Deceased | Veterans Affairs | [CSV](https://sourceforge.net/projects/entity-metadata/files/department_of_veterans_affairs/) |
| Public school | California Department of Education | [CSV](https://sourceforge.net/projects/entity-metadata/files/department_of_education/) |
| College | US Department of Education | [CSV](https://sourceforge.net/projects/entity-metadata/files/department_of_education/) |
| Radio and TV station | Wikidata | [CSV](https://sourceforge.net/projects/entity-metadata/files/wikidata/) |


## Using PetScan

PetScan is a simple way to get a list of articles in a category from Wikipedia.
For more advanced use, SPARQL might be better.

This is an example of how to export a list of articles in a category from PetScan.
The CSV includes the Wikidata IDs, which can be fed to the script `wikidata_org.py`
here to look up their metadata.

1. Go to [PetScan](https://petscan.wmflabs.org/)
2. Set categories to _Churches in the United States_
3. Click the *Wikidata* tab
4. Click the *Add items, where available* option
5. Click the *Output* tab
6. Click the *CSV* option
7. Click the *Do It* button

# Large files

The original and processed data sets can be very large, so most data
sets are not committed to this repository. Please use either

1. Download the original and use the programs here to process them, or
2. Download the processed files from the SourceForge repository.

# License

Written by Andrew Ziem. Copyright (c) 2017-2020 Compassion International.

The code is licensed under the [GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.en.html),
and the data sets belong to the original data owners. Please consult the original
sources for data licenses.

# Other resources

* [IMDb](https://www.imdb.com/interfaces/): full names of people who worked on movies in TSV
* [Indian names](https://www.kaggle.com/chaitanyapatil7/indian-names): given names of each gender in CSV
* [Open Library data dumps](https://openlibrary.org/developers/dumps): names of authors in JSON format
* [Museum of Modern Art](https://github.com/MuseumofModernArt/collection): names of 26K artists and 81K artworks
* [Polish first and last names](https://www.kaggle.com/djablo/list-of-polish-first-and-last-names): separate given female names, given male names, and surnames in separate text files
* [Social Security Administration](https://www.ssa.gov/oact/babynames/limits.html): baby names by year of birth and sex
* [Tinder female profiles](https://www.kaggle.com/immune/tinder-female-profiles) with given names
* [Voter registration](https://github.com/pablobarbera/voter-files): Python scripts to parse United States voter files, separate for each state
* [Federal Election Commission](https://classic.fec.gov/disclosurep/PDownload.do): donations to elections
* [Social Security Death Master File](http://ssdmf.info/): people with a Social Security Number who died

### Roster of professional licenses

* [Colorado: Department of Regulatory Agencies](https://apps.colorado.gov/dora/licensing/Lookup/GenerateRoster.aspx)
* [Connecticut](https://www.elicense.ct.gov/lookup/generateroster.aspx)
* [Florida: Department of Business and Professional Regular](http://www.myfloridalicense.com/DBPR/instant-public-records/)
* [Maine: Professional and Financial Regulation](https://www.maine.gov/pfr/professionallicensing/license_search.html)
* [Mississippi: Medical License](https://www.ms.gov/medical_licensure/renewal/rosterInstructions.jsp)
* [Texas: Engineers](http://engineers.texas.gov/downloads.htm#roster)
* [Virginia: Accountants](http://secure1.boa.virginia.gov/verification/)
* [Licensing Sources in State Agency Databases](https://godort.libguides.com/licensingdbs)


### Lists of names of businesses from government sources

* [California: Businesses](https://github.com/datadesk/california-business-entities)
* [Colorado: Businesses](https://data.colorado.gov/Business/Business-Entities-in-Colorado/4ykn-tg5h)

# Contact information

While this repository contains names of entities and some other metadata, this
repository does *not* contain any contact information: mailing address,
email address, telephone number, etc.


# Search keywords

* entity
* human
* person
* name
* first name
* given name
* surname
* family name
* church


