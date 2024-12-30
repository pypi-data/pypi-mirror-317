from academicdb import database, researcher, orcid, utils, publication
import pandas as pd

r = researcher.Researcher('./examples/config.toml')

r.get_publications()

bad_ids = pd.read_csv('./examples/bad_ids.csv')


all_pmids = [str(pub['PMID']) for pub in r.publications.values() if pub is not None and pub['PMID'] is not None]
for idx in bad_ids.index:
    id = bad_ids.loc[idx, 'idval'].strip()
    idtype = bad_ids.loc[idx, 'idtype'].strip()
    if idtype == 'doi':
        if id in r.publications:
            del r.publications[id]
            print(f'Dropping excluded publication {id}')
        else:
            print(f'Excluded doi {id} not found')
    elif idtype == 'pmid':
        if id in all_pmids:
            del_id = [k for k, v in r.publications.items() if v is not None and str(v['PMID']) == id]
            if len(del_id) > 0:
                del r.publications[del_id[0]]
                print(f'Dropping excluded publication {id}')
        else:
            print(f'Excluded pmid {id} not found')
