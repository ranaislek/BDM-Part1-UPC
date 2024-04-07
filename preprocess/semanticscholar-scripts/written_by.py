import json
import requests
import time
import csv
import pandas as pd
#read json file
raw_paper_data = None

path = "/home/furkanbk/BDM/BDM-P1/papers_json" # change the absolute path of data to your own path

top_subjects_dict = {
    "Computer Science": ["Machine Learning", "Artificial Intelligence"],
    "Chemistry": ["Organic", "Physical"],
    "Biology": ["Genetics", "Ecology"],
    "Business": ["Management", "Marketing"],
    "Law": ["Criminal", "International"]
}

paper_search_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

# Define headers with API key
headers = {'X-API-KEY': api_key}

author_details = []
def get_author_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id
    
    # Define which details about the paper you would like to receive in the response
    
    authors_url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id + '/authors'

    #find main author
    #paper_data_query_params = {'fields': 'authors.authorId'}
    paper_main_author_params = {'fields': 'name'}
    response = requests.get(authors_url, params=paper_main_author_params, headers=headers)
    #get all the authors
    #wait for 0.5 seconds
    time.sleep(0.5)
    authors = response.json()['data']
    # print(authors)

    #create a dictionary pairs that maps paperId to authorId

    for author in authors:
        authorId = author['authorId']

        author_details.append({'paperId': paper_id, 'authorId': authorId})

for field, subjects in top_subjects_dict.items():
    for subject in subjects:
        #start timer
        author_details = []
        start = time.time()
        with open(path + f'/matched_papers_{field}_{subject}.json', 'r') as json_file:
            raw_paper_data = json.load(json_file)


            #extract paperId from raw_paper_data
            paper_ids = [paper['paperId'] for paper in raw_paper_data]

            # Fetch paper details for each paper_id
            

            for paper_id in paper_ids:
                get_author_data(paper_id)

            df = pd.DataFrame(author_details)
            print(df.head())
            path_data = "/home/furkanbk/BDM/BDM-P1/data/written_by"
            #create a folder for each field and subject
            
            df.to_csv(f'{path_data}/{field}_{subject}_written_by.csv', index=False)
            print(f"Saved written by details for {field} - {subject} - Time taken: {time.time() - start}")
print("done")





   
   

 
    


