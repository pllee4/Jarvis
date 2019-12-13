import sqlite3
import pandas as pd
import voice

conn = sqlite3.connect('CrowdSourcingMandarin.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

dataFromBryan = [
    (22, 'Male', 'Yes', 2, 'Path1'),
    (21, 'Female', 'No', 4, 'Path2'),
    (20, 'Male', 'Yes', 3, 'Path3') 
    ]
    

def returnAttributes():
    return (22, 'Male', 'Yes', 3,
            'E:\Academic Year 4 201920\Sem7\Software Engineering\Project1')


class VoiceTable():
    
    def __init__(self):
        self.createVoiceTable()
        
    def createVoiceTable(self):
        c.execute('''CREATE TABLE IF NOT EXISTS VoiceTable(VoiceId INTEGER PRIMARY KEY AUTOINCREMENT, Voice TEXT UNIQUE)''')

    def insertToVoiceTable(self, voice):
        # for index, value in enumerate(command, start = 1):
        self.voice = voice
        for value in self.voice:
            c.execute('''INSERT OR IGNORE INTO VoiceTable(Voice)
                              VALUES (?)''', [value])
        conn.commit()
    
    def getVoice(self):
        return self.voice

        
def createTable():
    c.execute('''CREATE TABLE IF NOT EXISTS CrowdSourcingMandarin(ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                 Age INTEGER, Gender TEXT, NativeSpeaker TEXT, VoiceId INTEGER, DownloadLink TEXT UNIQUE,
                 FOREIGN KEY (VoiceId) REFERENCES VoiceTable (VoiceId))''')

def insertData():
    c.executemany('''INSERT OR IGNORE INTO CrowdSourcingMandarin(Age, Gender, NativeSpeaker, VoiceId, DownloadLink)
                     VALUES (?, ?, ?, ?, ?)''',
                dataFromBryan)
    conn.commit()


def init():
    MandarinTable = VoiceTable()
    MandarinTable.insertToVoiceTable(voice.voice)
    createTable()
    insertData()    
    c.close()
    conn.close()