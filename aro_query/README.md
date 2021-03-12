# aro_query

This Python script will query a user-specified section of [CARD's Antibiotic Resistance Ontology](https://github.com/arpcard/aro/blob/master/README.md), extracting it to a csv file for further use.

For more information about McMaster University's CARD (Comprehensive Antibiotic Resistance Database) project, please see [their website](https://card.mcmaster.ca/). The Antibiotic Resistance Ontology (ARO) is a controlled vocabulary, or hierarchy of terms, developed as part of this project. There are many different ways that a term within the ARO can be related to other ARO terms. For example, "diffusion method" is a subclass of the term "in-vitro microbial susceptibility test", and "disk diffusion method" is in turn a subclass of the "diffusion method" term. 

This script allows you to specify a particular term at which to "start" your query; it will extract all subclasses of this starting term to the csv file. You can also specify a depth, which tells the script where in the hierarchy of terms to stop your query. For instance, a depth of 1 would stop the query script after grabbing just the subclasses of the starting term. In terms of our susceptibility test example, a query starting with "in-vitro microbial susceptibility test" and with a depth of 1 would pull a term such as "diffusion method", but not "disk diffusion method", since that is one level deeper. However, if you wanted to extract another level of subclasses (i.e. grab "disk diffusion method" as well as "diffusion method"), you would specify a depth of 2.


## Getting Started

1. Install Python 3.8 if you haven't already (for installation instructions see [here](https://goto.iam.amr.pub/python-install))
1. Download CARD's latest ontology
1. Create an account with [WebProtege](https://webprotege.stanford.edu/), a user interface for viewing and exploring ontologies that will allow you to determine the "start" and "end" points of your query
1. Download CARD's [latest version of the ARO here](https://card.mcmaster.ca/latest/ontology).
- Right-click on the download, select `7-Zip/Extract Files...` and select a location for the tar file.
- Navigate to the tar folder you just created, right-click on the `card-ontology.tar` file that's inside the folder, and select `7-Zip/Extract Here`
- You should now see a file called `aro.owl` within this directory
1. Load `aro.owl` into WebProtege for viewing, and select "Entities" to view a hierarchy of all of the terms in the ontology
1. Determine your query's starting term and depth

**Note**: An explanation of how to use WebProtege to explore the ARO is out of the scope of these instructions, but more information can be found at the [WebProtege User Guide](https://protegewiki.stanford.edu/wiki/WebProtegeUsersGuide).

## Instructions

1. Clone this repository to your local computer
1. Open a Windows PowerShell window from the location this repository is saved to
1. Enter `pipenv install` to load the dependencies you'll need to run the script
1. Run the query with: `python aro_query.py <start_aro> <depth>`
   - `<start_aro>` is the ARO accession number for the starting point of your query, i.e. `ARO_3004388`, which corresponds to `in-vitro microbial susceptibility test`
   - `<depth>` specifies how many "levels" of subclasses downwards from the start term that you'd like to extract to your csv
   - For example: `python aro_query.py ARO_3004388 2` will extract all of the subclasses of the term with the identifier `ARO_3004388`. Since the `<depth>` argument is set to `2`, it will also extract any subclasses of the terms identified as subclasses of the starting identifier.

## Output

The script returns a csv file called `aro_query.csv`. It has 2 columns: 

- **ARO_id**: the accession number (unique identifier) for the term, designated by 

- **label**: a unique textual description of the term, also designated by CARD
