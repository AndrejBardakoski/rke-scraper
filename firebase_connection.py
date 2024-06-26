import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from document_name_parser import document_name_parser


class FirebaseConnectionService:

    def __init__(self):
        cred = credentials.Certificate('firebase-connection.json')
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def push_data(self, collection_name, document_name, data):
        parsed_document_name = document_name_parser(document_name)
        doc_ref = self.db.collection(collection_name).document(parsed_document_name)
        doc_ref.set({"data": data})

    # ===PUSH AGGREGATED DATA===
    def push_timeline_data(self, document_name, data):
        parsed_document_name = document_name_parser(document_name)
        doc_ref = self.db.collection("timeline").document(parsed_document_name)
        doc_ref.set(data, merge=True)

    def read_warehouse_data(self):
        docs = self.db.collection("warehouse").stream()

        for doc in docs:
            data = doc.to_dict()

            # print(f'{doc.id} => {data}')

            obj = {}
            # the key is the date
            keys = list(data.keys())

            for key in keys:
                obj[key] = data[key]['price']

            timeline_obj = {"category": data[keys[0]]['category'],
                            'name': data[keys[0]]['name'],
                            'unit': data[keys[0]]['unit'],
                            'timeline': obj}

            self.push_timeline_data(data[keys[0]]['name'], timeline_obj)
