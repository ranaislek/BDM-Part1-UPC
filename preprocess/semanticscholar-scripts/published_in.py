import json
import requests
import time
#convert this list of dictionaries to a csv file
import csv
import pandas as pd
#read json file

paper_search_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

# Define headers with API key
headers = {'X-API-KEY': api_key}

top_subjects_dict = {
    "Computer Science": ["Machine Learning", "Artificial Intelligence"],
    "Chemistry": ["Organic", "Physical"],
    "Biology": ["Genetics", "Ecology"],
    "Business": ["Management", "Marketing"],
    "Law": ["Criminal", "International"]
}


path = "/home/furkanbk/BDM/BDM-P1/papers_json" 

# Fetch paper details for each paper_id
conference_venues = []
journal_venues = []
published_in = []

def get_paper_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id

    #paper_data_query_params = {'fields': 'title,abstract,year,authors.authorId,embedding.specter_v2,venue,publicationVenue, journal'}
    paper_data_query_params = {'fields': 'publicationVenue'}
    
    
    #Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params, headers=headers)
   
    if response.status_code == 200:
        response = response.json()
        venue = response["publicationVenue"]

        if(venue is None):
            print(f"Venue is None for paper ID: {paper_id}")
        
            return None
        if("type" not in venue):
            print(f"Type is not in venue for paper ID: {paper_id}")
            return None
        
        if(venue["type"] == "journal"):
            id = venue["id"] if "id" in venue else None
            issn = venue["issn"] if "issn" in venue else None
            venue_url = venue["url"] if "url" in venue else None
            name = venue["name"] if "name" in venue else None

            journal_venues.append({"ss_venue_id": id, "name": name, "issn": issn, "url": venue_url})
            published_in.append({"paper_id": paper_id, "ss_venue_id": id})
            #print(f"Journal: {name}, ISSN: {issn}, URL: {venue_url}")
        
        elif(venue["type"] == "conference"):
            id = venue["id"] if "id" in venue else None
            name = venue["name"] if "name" in venue else None
            conference_url = venue["url"] if "url" in venue else None

            conference_venues.append({"ss_venue_id": id, "name": name, "url": conference_url}) 
            published_in.append({"paper_id": paper_id, "ss_venue_id": id})
            #print(f"Conference: {name}, URL: {conference_url}")


        
        return response
    else:
        print(f"Failed to fetch paper data for paper ID: {paper_id}")
        print(response.status_code)
        return None
   
total_time = 0
raw_paper_data = None
for field, subjects in top_subjects_dict.items():
    for subject in subjects:
        conference_venues = []
        journal_venues = []
        published_in = []
        
        #start timer
        start = time.time()
        with open(path + f'/matched_papers_{field}_{subject}.json', 'r') as json_file:
            raw_paper_data = json.load(json_file)

        #extract paperId from raw_paper_data
        paper_ids = [paper['paperId'] for paper in raw_paper_data]
        
        
        for paper_id in paper_ids:
            paper_data = get_paper_data(paper_id)

    
        df_published_in = pd.DataFrame(published_in)
        df_journal_venues = pd.DataFrame(journal_venues)
        df_conference_venues = pd.DataFrame(conference_venues)

        path_conferences = "/home/furkanbk/BDM/BDM-P1/data/semanticscholar/conferences"
        path_journals = "/home/furkanbk/BDM/BDM-P1/data/semanticscholar/journals"
        path_published_in = "/home/furkanbk/BDM/BDM-P1/data/semanticscholar/published_in"    
            
        df_published_in.to_csv(f'{path_published_in}/{field}_{subject}_published_in.csv', index=False)
        df_journal_venues.to_csv(f'{path_journals}/{field}_{subject}_journals.csv', index=False)
        df_conference_venues.to_csv(f'{path_conferences}/{field}_{subject}_conferences.csv', index=False)

        total_time += time.time() - start
        print(f"Saved conference-journa-publish details for {field} - {subject} - Time taken: {time.time() - start}")

