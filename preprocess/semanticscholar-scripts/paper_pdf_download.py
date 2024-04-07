import json
import requests
import time

from pathlib import Path


#read json file
raw_paper_data = None
path = "/home/furkanbk/BDM/BDM-P1/papers_json" # change the absolute path of data to your own path
path_pdf = "/home/furkanbk/BDM/BDM-P1/papers_pdf" # change the absolute path of data to your own path


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

def get_pdf_link(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id

    
    #paper_data_query_params = {'fields': 'title,abstract,year,embedding.specter_v2,'}
    paper_data_query_params = {'fields': 'openAccessPdf'}
    
    #Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params, headers=headers)
   
    if response.status_code == 200:
        response = response.json()
        if response['openAccessPdf'] != None:
            return response['openAccessPdf']
        else:
            return None
    else:
        print(response.status_code)
        return None
   
def download_pdf(paper_id, pdf_link, field, subject):
    
    response = requests.get(pdf_link["url"])
    if response.status_code == 200:
        #create a folder for each field and subject
        # Specify the path of the directory to be created
        folder_path = Path(f"{path_pdf}/{field}/{subject}")

        # Check if the directory already exists
        if not folder_path.exists():
            # Create the directory
            folder_path.mkdir(parents=True, exist_ok=False)

        else:
            print("Folder already exists.")
        
        #download the pdf file to the folder
        with open(f"{folder_path}/{paper_id}.pdf", 'wb') as pdf_file:
            pdf_file.write(response.content)
            #wait for 1 second
            time.sleep(1)
        print(f"Downloaded PDF for paper ID: {paper_id}")
    else:
        print(f"Failed to download PDF for paper ID: {paper_id}")

for field in top_subjects_dict.keys():
    for subject in top_subjects_dict[field]:
        with open(path + f'/matched_papers_{field}_{subject}.json', 'r') as json_file:
            paper_link = json.load(json_file)
            #print(len(paper_data)) 

            #extract paperId from raw_paper_data
            paper_ids = [paper['paperId'] for paper in paper_link]

            # Fetch paper details for each paper_id
            #pdf_links = []
            for paper_id in paper_ids:
                paper_link = get_pdf_link(paper_id)
                if paper_link is not None:
                    download_pdf(paper_id, paper_link, field, subject)
                else:
                    print(f"Failed to retrieve paper details for paper ID: {paper_id}")
                #time.sleep(0.5)  # Add a short delay to avoid hitting rate limits
            #convert this list of dictionaries to a csv file
            
            #download all the links






# import csv
# import pandas as pd
# df = pd.DataFrame(pdf_links)
# print(df.head())
#df.to_csv('papers_details.csv', index=False)
print("done")

