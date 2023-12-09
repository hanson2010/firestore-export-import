import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Firestore:

    def __init__(self, cred_file, project):
        cred = credentials.Certificate(cred_file)
        app = firebase_admin.initialize_app(cred, {'projectId': project})
        self.db = firestore.client(app)

    def get_collection(self, collection_name):
        return self.db.collection(collection_name)

    def read_all(self, collection_name):
        collection = self.get_collection(collection_name)
        return [snapshot.to_dict() for snapshot in collection.get()]

    def get_all_collections(self):
        return [collection.id for collection in self.db.collections()]

    def get_all_properties(self, collection_name):
        collection = self.get_collection(collection_name)
        documents = collection.stream()
        all_properties = set()

        for doc in documents:
            doc_dict = doc.to_dict()
            all_properties.update(doc_dict.keys())

        return list(all_properties)
