# Entity Metadata

This repository contains code and data about people and organizations.
Potential uses include training and evaluation data sets to:

* Classify names as a person or a church
* Capitalize names with the proper case such as _McGregory_ or _de la Cruz_
* Improve the [probablepeople](https://github.com/datamade/probablepeople) parser library
* [Generate names](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)

# Data sets

| Entity  | Source | Download |
|-----------|----------------------------------------------------------|------------------------------------------------------------------------------|
| Physician | CMS | [CSV](https://sourceforge.net/projects/entity-metadata/files/cms_physician/) |
| Author | [Open Library](https://openlibrary.org/developers/dumps) | [CSV](https://sourceforge.net/projects/entity-metadata/files/open_library/) |
| Person | Wikidata | [CSV](https://sourceforge.net/projects/entity-metadata/files/wikidata_person_bio/)
| Church | Wikidata via PetScan | [CSV](https://sourceforge.net/projects/entity-metadata/files/wikidata_church/) |


## Using PetScan

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

The original and processed data sets can be very large, so some data
sets may not be committed to this repository. Please use the links to
download the files from their original sources.

# License

The code is licensed under the [GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.en.html),
and the data sets belong to the original data owners.

# Other resources

* [Social Security Administration](https://www.ssa.gov/oact/babynames/limits.html): baby names by year of birth and sex
* [IMDb](https://www.imdb.com/interfaces/): full names of people who worked on movies in TSV
* [Voter registration](https://github.com/pablobarbera/voter-files): Python scripts to parse United States voter files, separate for each state
* [Polish first and last names](https://www.kaggle.com/djablo/list-of-polish-first-and-last-names): separate given female names, given male names, and surnames in separate text files
* [Tinder female profiles](https://www.kaggle.com/immune/tinder-female-profiles) with given names
* [Indian names](https://www.kaggle.com/chaitanyapatil7/indian-names): given names of each gender in CSV
* [Open Library data dumps](https://openlibrary.org/developers/dumps): names of authors in JSON format

### Roster of professional licenses

* [Colorado: Department of Regulatory Agencies](https://apps.colorado.gov/dora/licensing/Lookup/GenerateRoster.aspx)
* [Connecticut](https://www.elicense.ct.gov/lookup/generateroster.aspx)
* [Florida: Department of Business and Professional Regular](http://www.myfloridalicense.com/DBPR/instant-public-records/)
* [Maine: Professional and Financial Regulation](https://www.maine.gov/pfr/professionallicensing/license_search.html)
* [Mississippi: Medical License](https://www.ms.gov/medical_licensure/renewal/rosterInstructions.jsp)
* [Texas: Engineers](http://engineers.texas.gov/downloads.htm#roster)
* [Virginia: Accountants](http://secure1.boa.virginia.gov/verification/)
* [Licensing Sources in State Agency Databases](https://godort.libguides.com/licensingdbs)

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


