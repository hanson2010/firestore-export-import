import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Firestore:

    def __init__(self):
        self._client = self._connect()

    def get_collection(self, collection_name):
        return self._client.collection(collection_name)

    def read_all(self, collection_name):
        collection = self.get_collection(collection_name)
        return [snapshot.to_dict() for snapshot in collection.get()]

    def read_all_with_id(self, collection_name):
        collection = self.get_collection(collection_name)
        return [{'id': snapshot.id, 'doc': snapshot.to_dict()} for snapshot in collection.get()]

    def get_all_collections(self):
        return [collection.id for collection in self._client.collections()]

    def get_all_properties(self, collection_name):
        collection = self.get_collection(collection_name)
        documents = collection.stream()
        all_properties = set()

        for doc in documents:
            doc_dict = doc.to_dict()
            all_properties.update(doc_dict.keys())

        return list(all_properties)

    def _connect(self):
        env_name1 = 'GOOGLE_APPLICATION_CREDENTIALS'
        env_name2 = 'GOOGLE_CLOUD_PROJECT'
        # Check if the environment variable exists
        if env_name1 not in os.environ:
            print(f'Error: Environment variable "{env_name1}" is not defined.')
            exit(1)
        if env_name2 not in os.environ:
            print(f'Error: Environment variable "{env_name2}" is not defined.')
            exit(1)
        env_value1 = os.environ[env_name1]
        print(f'Firestore credential is at {env_value1}')
        env_value2 = os.environ[env_name2]
        print(f'Firestore project is {env_value2}')

        cred = credentials.Certificate(Path(env_value1))
        app = firebase_admin.initialize_app(cred, {'projectId': env_value2})
        return firestore.client(app)
