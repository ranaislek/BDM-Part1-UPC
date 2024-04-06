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

def get_paper_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id
    
    # Define which details about the paper you would like to receive in the response
    
    authors_url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id + '/authors'


    

    #find main author
    #paper_data_query_params = {'fields': 'authors.authorId'}
    paper_main_author_params = {'fields': 'name'}
    response = requests.get(authors_url, params=paper_main_author_params, headers=headers)
    #get the first author name
    # print(response.json()['data'][0]['name'])
    name = None
    if response.status_code == 200:
        if len(response.json()['data']) > 0:
            name = response.json()['data'][0]['name']
    email = None

    #paper_data_query_params = {'fields': 'title,abstract,year,authors.authorId,embedding.specter_v2,venue,publicationVenue, journal'}
    paper_data_query_params = {'fields': 'title,abstract,year,embedding.specter_v2'}
    
    
    #Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params, headers=headers)
   
    if response.status_code == 200:
        response = response.json()
        response['MA_name'] = name
        response['MA_email'] = email
        return response
    else:
        print(response.status_code)
        return None
   

for field, subjects in top_subjects_dict.items():
    for subject in subjects:
        #start timer
        start = time.time()
        with open(path + f'/matched_papers_{field}_{subject}.json', 'r') as json_file:
            raw_paper_data = json.load(json_file)

            #extract paperId from raw_paper_data
            paper_ids = [paper['paperId'] for paper in raw_paper_data]

            # Fetch paper details for each paper_id
            paper_details = []
            for paper_id in paper_ids:
                paper_data = get_paper_data(paper_id)
                if paper_data is not None:
                    paper_details.append(paper_data)
                else:
                    print(f"Failed to retrieve paper details for paper ID: {paper_id}")
                
            df = pd.DataFrame(paper_details)
            print(df.head())
            # save the paper details to a csv file in data folder
            path_data = "/home/furkanbk/BDM/BDM-P1/data/paper_details"
            #create a folder for each field and subject
            
            df.to_csv(f'{path_data}/{field}_{subject}_papers_details.csv', index=False)
            print(f"Saved paper details for {field} - {subject} - Time taken: {time.time() - start}")
print("done")

