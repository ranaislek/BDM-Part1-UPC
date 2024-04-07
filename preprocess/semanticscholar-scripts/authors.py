import pandas as pd
import json
import requests
import csv
import time

#read the csv residing in the data folder

path = "/home/furkanbk/BDM/BDM-P1/data/semanticscholar/written_by" # change the absolute path of data to your own path

top_subjects_dict = {
    "Computer Science": ["Machine Learning", "Artificial Intelligence"],
    "Chemistry": ["Organic", "Physical"],
    "Biology": ["Genetics", "Ecology"],
    "Business": ["Management", "Marketing"],
    "Law": ["Criminal", "International"]
}

# Define the base URL for the author details endpoint
base_url = "https://api.semanticscholar.org/graph/v1/author/"

# Define headers with API key
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

headers = {'X-API-KEY': api_key}


def get_author_details(author_id):
    #convert the author_id to string and eliminate the decimal point
    author_id = str(author_id).split('.')[0]
    url = base_url + str(author_id)
    
    response = requests.get(url, params=author_data_query_params, headers=headers)
    #wait for 0.5 seconds
    time.sleep(0.5)
    if response.status_code == 200:
        response = response.json()
        if(response['affiliations'] == []):
            
            response['affiliations'] = None
            
        # elif(len(response['affiliations']) > 1):
        #     response['affiliations'] = response['affiliations'][0]
        
       
        return response
    else:
        return None
total_time = 0
#read the csv file
for field, subjects in top_subjects_dict.items():
    for subject in subjects:
        start = time.time()
        df = pd.read_csv(path + f'/{field}_{subject}_written_by.csv')
    

        author_ids = df['authorId'].unique()



        # Define the fields you would like to receive in the response
        author_data_query_params = {'fields': 'name,affiliations'}

        author_details = []

       
        for author_id in author_ids:
            author_data = get_author_details(author_id)
            print(author_data)
            if author_data is not None:
                author_details.append(author_data)
            else:
                print("Failed to retrieve author details for author_id:", author_id)
        df = pd.DataFrame(author_details)

        path_data = "/home/furkanbk/BDM/BDM-P1/data/semanticscholar/authors"
            #create a folder for each field and subject
            
        df.to_csv(f'{path_data}/{field}_{subject}_authors.csv', index=False)
        total_time += time.time() - start
        print(f"Saved authors details for {field} - {subject} - Time taken: {time.time() - start}")

print("done")
print("Total time taken: ", total_time)