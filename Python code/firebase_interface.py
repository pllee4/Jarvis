import firebase_admin
from firebase_admin import credentials, storage
import urllib.request, json
import os

folder_to_store = "..\\..\\voices"

class FirebaseInterface ():
    def __init__ (self):
        cred = credentials.Certificate(r"crowdsourcingmandarin-firebase-adminsdk-2pnx9-b4a6da0e8a.json")
        app2 = firebase_admin.initialize_app(cred,  {'storageBucket': r'crowdsourcingmandarin.appspot.com'}, name='storage')
        self.bucket = storage.bucket(app = app2)

    def run(self):
        blobs = self.bucket.list_blobs()

        database = []
        for blob in blobs:
            if blob.name != "voices/":
                path_to_save = folder_to_store + "\\" + str(len(os.listdir(r"..\..\voices")) + 1) + \
                "_" + blob.metadata.get('Word') + \
                "_" + blob.metadata.get('Native') + \
                "_" + blob.metadata.get('Gender') + \
                "_" + blob.metadata.get('Age') + \
                ".3gp"
                blob.download_to_filename(path_to_save)
                blob.delete()
                database.append((blob.metadata.get('Age'), blob.metadata.get('Gender'), blob.metadata.get('Native'), blob.metadata.get('Word'), path_to_save ))

        return database

#if __name__ == "__main__":
#    FB = FirebaseInterface()
#    print(FB.run())