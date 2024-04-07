import csv
from scholarly import scholarly

# List of fields to search for
fields = [
    "ecology", "genetics", "management", "marketing",
    "organic", "physical", "artificial intelligence",
    "machine learning", "criminal", "international"
]

def write_author_csv(authors, field):
    with open(f'{field}_authors.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Author Id', 'Name', 'Affiliation', 'Email',  'citedby','citedby5y','hindex','hindex5y','Interests' ])
        for author in authors:
            csvwriter.writerow([author['scholar_id'], author['name'], author['affiliation'], author.get('email_domain', ''),
                                author.get('citedby', ''),author.get('citedby5y', ''),author.get('hindex', ''),
                                author.get('hindex5y', ''),', '.join(author.get('interests', []))])

def write_paper_csv(authors, field):
    with open(f'{field}_papers.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Author-Paper Id', 'author_id', 'Title', 'Year', 'Citations'])
        for author in authors:
            for pub in author['publications'][:10]:  # Limit to first 10 publications
                pub_filled = scholarly.fill(pub)
                csvwriter.writerow([pub_filled['author_pub_id'], author['scholar_id'], pub_filled['bib']['title'], pub_filled['bib'].get('pub_year', ''), pub_filled['num_citations']])

def write_ap_csv(authors, field):
    with open(f'{field}_author_papers.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Author', 'Paper Title'])
        for author in authors:
            for pub in author['publications'][:10]:  # Limit to first 10 publications
                pub_filled = scholarly.fill(pub)
                csvwriter.writerow([author['name'], pub_filled['bib']['title']])

for field in fields:
    search_query = scholarly.search_keyword(field)
    authors = []
    try:
        for _ in range(10):  # Attempt to get up to 10 authors
            authors.append(scholarly.fill(next(search_query)))
    except StopIteration:
        print(f"Less than 10 authors found for {field}")

    if authors:
        write_author_csv(authors, field)
        write_paper_csv(authors, field)
        write_ap_csv(authors, field)
    else:
        print(f"No authors found for {field}")