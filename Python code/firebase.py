import firebase_admin
from firebase_admin import credentials, firestore, storage
import urllib.request, json


cred = credentials.Certificate(r"crowdsourcingmandarin-firebase-adminsdk-2pnx9-b4a6da0e8a.json")


app2 = firebase_admin.initialize_app(cred,  {
    'storageBucket': r'crowdsourcingmandarin.appspot.com'
}, name='storage')

bucket = storage.bucket(app = app2)
blob = bucket.blob('voices/audiorecord1.3gp')
# blob.download_to_filename(r"C:\Users\Teh\Documents\pythontest\softwareassgnment\127.3gp")

# blob.download_to_filename(r"DownloadFile\123.gp")

blobs = bucket.list_blobs()

# print(blob.metadata['Native'] for blob.metada in blobs)
for blob in blobs:
    # print(blob.metadata)
    # print(blob.name)
    print(blob.metadata)
    