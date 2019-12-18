import firebase_admin
from firebase_admin import credentials, storage
import urllib.request, json
import os

FOLDER_TO_STORE = "..\\..\\voices"


class FirebaseInterface ():
    """
    The class is written to interface with firebase.
    """ 

    def __init__ (self):
        """
        This method initialize the instances of FirebaseInterface.
        """    
        cred = credentials.Certificate(r"crowdsourcingmandarin-firebase-adminsdk-2pnx9-b4a6da0e8a.json")
        app2 = firebase_admin.initialize_app(cred,  {'storageBucket': r'crowdsourcingmandarin.appspot.com'}, name='storage')
        self.bucket = storage.bucket(app = app2)
        if (not os.path.exists(FOLDER_TO_STORE)):  
            os.makedirs(FOLDER_TO_STORE)

  
    def run(self):  
        """
        This method check for the available voices in firebase and download it to local storage.
        
        Returns:
        list: the list of downloaded voices with its attributes such as age, gender and words.
        """
        blobs = self.bucket.list_blobs()

        database = []
        for blob in blobs:
            if blob.name != "voices/":
                path_to_save = FOLDER_TO_STORE + "\\" + str(len(os.listdir(r"..\..\voices")) + 1) + \
                "_" + blob.metadata.get('Word') + \
                "_" + blob.metadata.get('Native') + \
                "_" + blob.metadata.get('Gender') + \
                "_" + blob.metadata.get('Age') + \
                ".3gp"
                blob.download_to_filename(path_to_save)
                blob.delete()
                database.append((blob.metadata.get('Age'), blob.metadata.get('Gender'), blob.metadata.get('Native'), blob.metadata.get('Word'), path_to_save ))

        return database