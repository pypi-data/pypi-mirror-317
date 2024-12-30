import scholarly
from datetime import datetime, timedelta

def get_collaborators(name, scholar_id):
    author = scholarly.search_author_id(scholar_id)

    if author is None:
        print(f"Error: Unable to fetch Google Scholar profile for {name} (ID: {scholar_id})")
        return

    author = scholarly.fill(author, sections=['publications'])
    recent_collaborators = set()
    time_limit = datetime.now() - timedelta(days=48 * 30)

    for publication in author['publications']:
        pub = scholarly.fill(publication)

        if 'year' in pub and 'authors' in pub:
            pub_year = pub['year']

            if pub_year >= time_limit.year:
                for author in pub['authors']:
                    if author['name'] != name:
                        recent_collaborators.add((author['name'], author.get('affiliation', 'Unknown')))

    return recent_collaborators


if __name__ == "__main__":
    name = 'Russell Poldrack' #input("Enter the name of the researcher: ")
    scholar_id = 'RbmLvDIAAAAJ' # input("Enter the Google Scholar ID of the researcher: ")

    collaborators = get_collaborators(name, scholar_id)

    if collaborators:
        print(f"\nCollaborators of {name} in the last 48 months:")
        for collaborator, affiliation in collaborators:
            print(f"{collaborator} ({affiliation})")
    else:
        print(f"No recent collaborators found for {name}.")
