import kivy
import sqlite3
import numpy as np
import pandas as pd
import database as db
import firebase_interface as fi

from random import randint

from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup   
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.config import Config

conn = sqlite3.connect('CrowdSourcingMandarin.db')
c = conn.cursor()
db.init()

Config.set('graphics', 'resizable', False)

class SpinnerOptions(SpinnerOption):

    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_color = (0.1, 0.2, 50, 0.5)    # blue colour
            
class CrowdSourcing(App):
    def build(self):                                                                    
        layout = GridLayout(cols=5, spacing = 1,size_hint_y=None)               
        layout.bind(minimum_height=layout.setter('height'))      
              
        self.age_btn = Spinner(                                              
                    text = 'Age',
                    option_cls = SpinnerOptions,
                    background_color = (1, 1, 50, 0.5 ),
                  )
        self.gender_btn = Spinner(                                           
                    text = 'Gender',     
                    option_cls = SpinnerOptions,
                    background_color = (1, 1, 50, 0.5 ),
                  )
        self.nativespeaker_btn = Spinner(                                              
                    text = 'NativeSpeaker',
                    option_cls = SpinnerOptions,
                    background_color = (1, 1, 50, 0.5 ),
                  )
        self.voiceid_btn = Spinner(
                    text = 'Voice',
                    option_cls = SpinnerOptions,
                    background_color = (1, 1, 50, 0.5 ),
                  )
        
        self.select_btn = Button(text = 'Select', size_hint_y=None, height=40, background_color = (1, 1.5, 50, 1))      

        self.age_btn.bind(text = self._ageSelected)                      
        self.gender_btn.bind(text = self._genderSelected)                
        self.nativespeaker_btn.bind(text = self._nativeSpeakerSelected)                          
        self.voiceid_btn.bind(text = self._voiceIdSelected)                    
        
        self.select_btn.bind(on_release = self._selected) 

        self.firebae_inteface = fi.FirebaseInterface()
        
        # self.message = Label(text = "Welcome", pos = (2900,900), font_size = '50sp', padding = (1000, 600))
        # self.message.bind(text = self._showMessage)
        
        layout.bind(minimum_height=layout.setter('height'))
        layout.add_widget(self.age_btn)                                      
        layout.add_widget(self.gender_btn)
        layout.add_widget(self.nativespeaker_btn)
        
        layout.add_widget(self.voiceid_btn)
        layout.add_widget(self.select_btn)
        
        # layout.add_widget(self.message)
    
        Window.bind(mouse_pos=self._mousePos)

        Clock.schedule_interval(self._updateDatabase, 2.0)

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))  
        root.add_widget(layout)
        return root
            
    def _ageSelected(self, instance, value):                                       
        instance.text = value
        self.GetAge.insertValue(value)
        
    def _genderSelected(self, instance, value):                                    
        instance.text = value
        self.GetGender.insertValue(value)
        
    def _nativeSpeakerSelected(self, instance, value):                             
        instance.text = value
        self.GetNativeSpeaker.insertValue(value)
        
    def _voiceIdSelected(self, instance, value):                                             
        instance.text = value
        c.execute('''SELECT DISTINCT VoiceId FROM VoiceTable WHERE ((Voice = ?))''', (value,))
        entry = c.fetchone()
        try:
            self.GetVoice.insertValue(entry[0])
        except:
            self.GetVoice.insertValue("All Commands")

    def _selected(self, instance):        
        AgeQuery = Query(self.GetAge, "DownloadLink", "CrowdSourcingMandarin", "All")
        GenderQuery = Query(self.GetGender, "DownloadLink", "CrowdSourcingMandarin", "All")
        NativeSpeakerQuery = Query(self.GetNativeSpeaker, "DownloadLink", "CrowdSourcingMandarin", "All")
        VoiceQuery = Query(self.GetVoice, "DownloadLink", "CrowdSourcingMandarin", "All Commands")        
        toBeDownloaded(AgeQuery,GenderQuery, NativeSpeakerQuery, VoiceQuery)
        
    def _mousePos(self, window, pos):
        if (pos[1] > 566 and pos[1] < 600):
            if (pos[0] > 1 and pos[0] < 156):
                self.age_btn.background_color = (0.3, 0.3, 50, 1)
            else:
                self.age_btn.background_color = (1, 1, 50, 0.5)
                
            if (pos[0] > 160 and pos[0] < 315):
                self.gender_btn.background_color = (0.3, 0.3, 50, 1)
            else:
                self.gender_btn.background_color = (1, 1, 50, 0.5)
                
            if (pos[0] > 320 and pos[0] < 477):     
                self.nativespeaker_btn.background_color = (0.3, 0.3, 50, 1)
            else:
                self.nativespeaker_btn.background_color = (1, 1, 50, 0.5)
                
            if (pos[0] > 482 and pos[0] < 638):    
                self.voiceid_btn.background_color = (0.3, 0.3, 50, 1)
            else:
                self.voiceid_btn.background_color = (1, 1, 50, 0.5)    
                
            if (pos[0] > 642 and pos[0] < 795):
                self.select_btn.background_color = (1, 1.5, 50, 1)
            else:
                self.select_btn.background_color = (0.8, 0.9, 50, 1)
        else:
            self.age_btn.background_color = (1, 1, 50, 0.5)
            self.gender_btn.background_color = (1, 1, 50, 0.5)
            self.nativespeaker_btn.background_color = (1, 1, 50, 0.5)
            self.voiceid_btn.background_color = (1, 1, 50, 0.5)                
            self.select_btn.background_color = (0.8, 0.9, 50, 1)
            
    def _updateDatabase(self, dt):
        #number = randint(1, 29)                                                     ##Sheng can delete this
        #db.dataFromFirebase = [(number, 'Male', 'Yes', number, str(number))]        ##Sheng put yr function here 
        db.dataFromFirebase = self.firebae_inteface.run()
        db.insertData(db.dataFromFirebase)
        db.dataFromFirebase = []
        self.age_btn.values = self.getAge()                 
        self.gender_btn.values = self.getGender() 
        self.nativespeaker_btn.values = self.getNativeSpeaker()                          
        self.voiceid_btn.values = self.getVoice()   

    def getAge(self):
        column = "Age"
        c.execute("SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin ORDER BY " + column + " ASC")
        self.GetAge = Fetch(c.fetchall(), column, "All")
        return self.GetAge.value()

    def getGender(self):
        column = "Gender"
        c.execute("SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin")
        self.GetGender = Fetch(c.fetchall(), column,  "All")
        return self.GetGender.value()

    def getNativeSpeaker(self):
        column = "NativeSpeaker"
        c.execute("SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin")        
        self.GetNativeSpeaker = Fetch(c.fetchall(), column, "All")
        return self.GetNativeSpeaker.value()
    
    def getVoice(self):
        column = "VoiceId"
        c.execute("SELECT DISTINCT Voice FROM VoiceTable WHERE VoiceId IN (SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin)")        
        self.GetVoice = Fetch(c.fetchall(), column, "All Commands")
        return self.GetVoice.value()

class Fetch():
    
    def __init__(self, data, column, extraData = None):
        self.data = data
        self.extraData = extraData
        self.column = column
    
    def value(self):
        returnData = []
        for value in self.data:
            returnData.append(str(value[0]))
        if self.extraData is not None:
            returnData.append(self.extraData)
        return returnData
    
    def getColumn(self):
        return str(self.column)
    
    def getValue(self):
        return str(self.value)
    
    def insertValue(self, value):
        self.value = value
        

class Query():
    
    def __init__(self, object, select, table, condition):
        self.column = object.getColumn()
        self.value = object.getValue()
        self.query = "SELECT " + select + " FROM " + table 
        if self.value != condition:
            self.query += " WHERE " + self.column + " = '" + self.value + "'"
    
    def getQuery(self):
        return self.query
   
    def getValue(self):
        return self.value

def toBeDownloaded(*argv):
    selection_query = ''
    value = []
    header = ["Age", "Gender", "NativeSpeaker", "Command"]
    for arg in argv:
        selection_query += arg.getQuery() + " INTERSECT "
        value.append(arg.getValue())
    selection_query = selection_query[:-len(" INTERSECT ")]
    
    parse_data = dict(zip(header, value))
    parse_data.update({'Path':[]})
    c.execute(selection_query)
    parse_data['Path'] = c.fetchall()    
    if len(parse_data['Path']) < 1:
        Alert(title='Oops!', text='Invalid inputs')
    else:
        print(parse_data)                                       ##@Sheng Enter your function here 
    
class Alert(Popup):

    def __init__(self, title, text):
        super(Alert, self).__init__()
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')
        content.add_widget(
            Label(text=text, halign='left', height  = 10)
        )
        ok_button = Button(text = 'OK' , size_hint_y=None, height=50)
        content.add_widget(ok_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(Window.width / 3, Window.height / 3),
            auto_dismiss=True,
        )
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
        
if __name__ == '__main__':                                                         ##run the app
    CrowdSourcing().run()
