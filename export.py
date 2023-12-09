import firebase_admin
from firebase_admin import credentials, firestore
import json

from helpers.csv import csv_writer


def process_collection(client, file_path, collection_name):
    fields = client.get_all_properties(collection_name)
    docs = client.read_all(collection_name)

    with open(file_path, 'w') as csv_file:
        writer = csv_writer(csv_file, fields)
        writer.writeheader()

        for doc in docs:
            writer.writerow(doc)



cred = credentials.Certificate('xxxxxx-xxxxxxxxx-xxxxxx-firebase-adminsdk-xxxxx-xxxxxxxxxx.json') # from firebase project settings
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://xxxxxx-xxxxxxxxx-xxxxxx.firebaseio.com'
})

db = firebase_admin.firestore.client()

# add your collections manually
collection_names = ['Admin', 'Approved', 'Crimes', 'Events']
collections = dict()
dict4json = dict()
n_documents = 0

for collection in collection_names:
    collections[collection] = db.collection(collection).get()
    dict4json[collection] = {}
    for document in collections[collection]:
        docdict = document.to_dict()
        dict4json[collection][document.id] = docdict
        n_documents += 1

jsonfromdict = json.dumps(dict4json)

path_filename = "./firestore.json"
print (("Downloaded %d collections, %d documents and now writing %d json characters to %s") % ( len(collection_names), n_documents, len(jsonfromdict), path_filename ))
with open(path_filename, 'w') as the_file:
    the_file.write(jsonfromdict)
