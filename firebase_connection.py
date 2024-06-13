import cyrtranslit
import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def document_name_parser(document_name):
    document_name = cyrtranslit.to_latin(document_name, 'mk')
    document_name = (document_name.strip().lower()
                     .replace(' ', '_')
                     .replace('ḱ', 'kj')
                     .replace('č', 'c')
                     .replace('š', 's')
                     .replace('ž', 'z')
                     .replace('ć', 'c')
                     .replace('đ', 'dj'))

    return document_name


class FirebaseConnection:
    def __init__(self):
        cred = credentials.Certificate('firebase-connection.json')
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def push_test_data(self):
        doc_ref = self.db.collection("users").document("alovelace")
        doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

    def push_data(self, collection_name, document_name, data):
        parsed_document_name = document_name_parser(document_name)
        doc_ref = self.db.collection(collection_name).document(parsed_document_name)
        doc_ref.set({"data": data})

    # TODO:  Implement a way to notify the user if the price has changed
    # This code should run daily to check for price changes
    def push_agg_data(self, document_name, data):
        parsed_document_name = document_name_parser(document_name)
        doc_ref = self.db.collection("warehouse").document(parsed_document_name)
        old_data_doc = doc_ref.get()
        if old_data_doc.exists:
            old_data = old_data_doc.to_dict()
            old_data[data['valid_from']] = data
            doc_ref.set(old_data)
        else:
            # If the document doesn't exist, set it with the new data
            doc_ref.set({data['valid_from']: data})
