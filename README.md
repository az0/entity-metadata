# Entity Metadata

This repository contains code and data about people and organizations.
Potential uses include training and evaluation data sets to:

* Classify names as a person or a church
* Capitalize names with the proper case such as _McGregory_ or _de la Cruz_
* Improve the [probablepeople](https://github.com/datamade/probablepeople) parser library
* [Generate names](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)

# Data sets

* [CMS Physician Compare National](https://www.healthdata.gov/dataset/physician-compare-national-downloadable-file)

* Churches in the United States: Category _Churches in the United States_ from PetScan

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

The code is licensed under the GNU General Public License version 3, and the data sets belong to the original data owners.