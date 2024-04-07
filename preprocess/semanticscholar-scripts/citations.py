import json
import requests
import time
#read json file
#convert this list of dictionaries to a csv file
import csv
import pandas as pd

path = "/home/furkanbk/BDM/BDM-P1/papers_json" # change the absolute path of data to your own path

top_subjects_dict = {
    "Computer Science": ["Machine Learning", "Artificial Intelligence"],
    "Chemistry": ["Organic", "Physical"],
    "Biology": ["Genetics", "Ecology"],
    "Business": ["Management", "Marketing"],
    "Law": ["Criminal", "International"]
}

raw_paper_data = None

paper_search_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

# Define headers with API key
headers = {'X-API-KEY': api_key}
# Fetch paper details for each paper_id
def get_reference_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id
    
    paper_data_query_params = {'fields': 'references'}

    #Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params, headers=headers)
   
    if response.status_code == 200:
        response = response.json()
        paperId = response['paperId']
        references = response['references']
        for reference in references:
            referenceId = reference['paperId']
            #create a new dictionary to store the paperId and referenceId
            reference_details.append({'paperId': paperId, 'referenceId': referenceId})
        
    else:
        print(response.status_code)
        


reference_details = []
total_time = 0
for field, subjects in top_subjects_dict.items():
    for subject in subjects:
        reference_details = []
        #start timer
        start = time.time()
        with open(path + f'/matched_papers_{field}_{subject}.json', 'r') as json_file:
            raw_paper_data = json.load(json_file)


        #extract paperId from raw_paper_data
        paper_ids = [paper['paperId'] for paper in raw_paper_data]

        for paper_id in paper_ids:
            get_reference_data(paper_id)

        df = pd.DataFrame(reference_details)

        path_citations = "/home/furkanbk/BDM/BDM-P1/data/citations"
        df.to_csv(f'{path_citations}/{field}_{subject}_citations.csv', index=False)
        print(f"Saved citation details for {field} - {subject} - Time taken: {time.time() - start}")
        total_time += time.time() - start

#df.to_csv('papers_details.csv', index=False)
print("done")

