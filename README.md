# Instructions on how to run: BDM-P1
Big Data Management and Analytics Project - Part 1

Github link: https://github.com/furkanbk/BDM-P1

For our startup ScholarIA, we need a database full of academic papers and related information.
To do that, as a start we used two datasources: Semanticscholar and Scholarly API

Requirements:

Scholarly:
$ pip install scholarly
- Then, run the file named 'multiple-authors-papers.py'.
- It will generate 20 csv files in total from 10 different fields which are:
"ecology", "genetics", "management", "marketing","organic", "physical", 
"artificial intelligence", "machine learning", "criminal", "international".
- 2 csv's per field -> one shows author-paper relation, the other gives more information about paper.

Semantic Scholar:
- An API key is necessary. There exists an API key in the files but we suggest creating your own and replacing variable api_key with it.
- Please change the absolute paths in python scripts to your own directories.
- It is necessary to keep the file structure as is due to csv writes in preprocess files are specifying absolute directory paths.

  Running order:
  - 1: bulk_paper_on_field.py (this will generate json files containing 100 paper ids for 10 fields)
  - 2: paper_details.py / published_in.py / written_by.py / citations.py / paper_pdf_download.py can be run in any order after stage 1.
  - 3: authors.py

  gii.py does not depend on above, only requires to find the downloaded raw-gii csv file.

  These files will generate csv,json and pdf files ready to import to S3 datalake.
