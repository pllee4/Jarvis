import sqlite3
import pandas as pd
import voice

conn = sqlite3.connect('CrowdSourcingMandarin.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

dataFromFirebase = [ ]
    


class VoiceTable():
    """
    The class is written to for creating of VoiceTable in database.
    """ 
    
    def __init__(self):
        """
        This method initialize the instances of VoiceTable.
        """   
        self.createVoiceTable()
        
    def createVoiceTable(self):
        """
        This method create the VoiceTable with VoiceId (Integer Primary Key) and Voice (Text Unique).
        """  
        c.execute('''CREATE TABLE IF NOT EXISTS VoiceTable(VoiceId INTEGER PRIMARY KEY,
                     Voice TEXT UNIQUE)''')

    def insertToVoiceTable(self, voice):
        """
        This method is to insert the Voice into VoiceTable.
        
        Parameters:
        voice (List): the list of voice would be inserted into the VoiceTable if it is not existed in VoiceTable
        """
        self.voice = voice
        for value in self.voice:
            c.execute('''INSERT OR IGNORE INTO VoiceTable(Voice)
                              VALUES (?)''', [value])
        conn.commit()
    
    def getVoice(self):
        
        """
        This method is to return the list of voice in VoiceTable
        
        Returns:
        list: the list of voice that is inserted into VoiceTable
        """
        return self.voice

        
def createTable():
    """
    This method is to create table of CrowdSourcingMandarin using sqlite3 command
    """
    c.execute('''CREATE TABLE IF NOT EXISTS CrowdSourcingMandarin (ID INTEGER PRIMARY KEY, 
                 Age INTEGER, Gender TEXT, NativeSpeaker TEXT, VoiceId INTEGER, DownloadLink TEXT UNIQUE,
                 FOREIGN KEY (VoiceId) REFERENCES VoiceTable (VoiceId)
                 )''')

def insertData(dataFromFirebase):
    """
    This method is to insert data from Firebase into table of CrowdSourcingMandarin using sqlite3 command
    
    Parameters:
    dataFromFirebase(list): the list of data which are consisted of Age, Gender, NativeSpeaker, VoiceId, DownloadLink
    """ 
    c.executemany('''INSERT OR IGNORE INTO CrowdSourcingMandarin(Age, Gender, NativeSpeaker, VoiceId, DownloadLink)
                     VALUES (?, ?, ?, ?, ?)''',
                dataFromFirebase)
    conn.commit()


def init():
    """
    This method is to create instance of VoiceTable, insert the data into VoiceTable and create table of CrowdSourcingMandarin 
    """
    MandarinTable = VoiceTable()
    MandarinTable.insertToVoiceTable(voice.voice)
    createTable()
    # insertData(dataFromFirebase)    
    # c.close()
    # conn.close()