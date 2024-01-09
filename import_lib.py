import json
from pathlib import Path


def import_collections(client, collections_exclude='', input_dir='./json'):
    collections = client.get_all_collections()
    filtered_collections = list([collection for collection in collections if collection not in collections_exclude])

    for collection in filtered_collections:
        process_collection(client,
                           collection,
                           Path(f'{input_dir}/{collection}.json'))


def process_collection(client, collection, file_path, file_type='json'):
    docs = client.read_all_with_id(collection)

    str = ''
    with open(file_path, 'r', encoding='utf-8') as json_file:
        str = json_file.read()
    
    dict = json.loads(str)
    doc_ref = collection.document(dict['id'])
    doc_ref.set(dict['doc'])

    print(f'Wrote {len(docs)} documents to collection {collection}')
