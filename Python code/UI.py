
import kivy
import sqlite3
import numpy as np
import pandas as pd
import database as db
import os
import shutil

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

import firebase_interface as fi

conn = sqlite3.connect('CrowdSourcingMandarin.db')
c = conn.cursor()
db.init()

Config.set('graphics', 'resizable', False)

path_to_saved = "..\\..\\"


class SpinnerOptions(SpinnerOption):
    """
    The class is written to for creating SpinnerOptions
    """ 

    def __init__(self, **kwargs):
        """
        This method initialize the instances of SpinnerOptions.
        """   
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_color = (0.1, 0.2, 50, 0.5)    # blue colour
            
class CrowdSourcing(App):
    """
    The class is written to create CrowdSourcing App
    
    Parameters:
    App(Inheritance of class): To inherit the class of App from kivy.app
    """ 
    def build(self):  
        """
        This method builds the application with 4 spinners and one select button
        
        Returns:
        object: the instance of ScrollView
        """                                                                    
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
        
        self.GetAge = Fetch("Age", "All")
        self.GetGender = Fetch("Gender",  "All")
        self.GetNativeSpeaker = Fetch("NativeSpeaker", "All")
        self.GetVoice = Fetch("VoiceId", "All Commands")
        
        self.age_btn.values = self.getAge()                 
        self.gender_btn.values = self.getGender() 
        self.nativespeaker_btn.values = self.getNativeSpeaker()                          
        self.voiceid_btn.values = self.getVoice()  
        
        self.firebase_inteface = fi.FirebaseInterface()
        
        layout.bind(minimum_height=layout.setter('height'))
        layout.add_widget(self.age_btn)                                      
        layout.add_widget(self.gender_btn)
        layout.add_widget(self.nativespeaker_btn)
        
        layout.add_widget(self.voiceid_btn)
        layout.add_widget(self.select_btn)
        
    
        Window.bind(mouse_pos=self._mousePos)

        Clock.schedule_interval(self._updateDatabase, 5)

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))  
        root.add_widget(layout)
        return root
            
    def _ageSelected(self, instance, value):  
        """
        The method is called when age_btn is clicked. It would update the value of button according to the selection
        
        Parameters:
        instance (object): The instance of the button
        value (str): The value that would to become the text of instance
        """                                      
        instance.text = value
        self.GetAge.insertValue(value)
        
    def _genderSelected(self, instance, value):     
        """
        The method is called when gender_btn is clicked. It would update the value of button according to the selection
        
        Parameters:
        instance (object): The instance of the button
        value (str): The value that would to become the text of instance
        """                                   
        instance.text = value
        self.GetGender.insertValue(value)
        
    def _nativeSpeakerSelected(self, instance, value):  
        """
        The method is called when nativespeaker_btn is clicked. It would update the value of button according to the selection
        
        Parameters:
        instance (object): The instance of the button
        value (str): The value that would to become the text of instance
        """                               
        instance.text = value
        self.GetNativeSpeaker.insertValue(value)
        
    def _voiceIdSelected(self, instance, value):  
        """
        The method is called when voiceid_btn is clicked. It would update the value of button according to the selection
        
        Parameters:
        instance (object): The instance of the button
        value (str): The value that would to become the text of instance
        """                                               
        instance.text = value
        c.execute('''SELECT DISTINCT VoiceId FROM VoiceTable WHERE ((Voice = ?))''', (value,))
        entry = c.fetchone()
        try:
            self.GetVoice.insertValue(entry[0])
        except:
            self.GetVoice.insertValue("All Commands")

    def _selected(self, instance):  
        """
        The method is called when select_btn is clicked. It would update the value of button according to the selection
        
        Parameters:
        instance (object): The instance of the button
        """    
        
        AgeQuery = Query(self.GetAge, "DownloadLink", "CrowdSourcingMandarin", "All")
        GenderQuery = Query(self.GetGender, "DownloadLink", "CrowdSourcingMandarin", "All")
        NativeSpeakerQuery = Query(self.GetNativeSpeaker, "DownloadLink", "CrowdSourcingMandarin", "All")
        VoiceQuery = Query(self.GetVoice, "DownloadLink", "CrowdSourcingMandarin", "All Commands")   
        toBeDownloaded(AgeQuery,GenderQuery, NativeSpeakerQuery, VoiceQuery)
        
    def _mousePos(self, window, pos):
        """
        The method is to read the position of mouse in window
        
        Parameters:
        window (object): window of the application
        pos(array): The value of position of mouse
        """    
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
        """
        The method is to update the data in database according to new input from firebase
        
        Parameters:
        dt (float): the interval time of updating the function 
        """  
        db.dataFromFirebase = self.firebase_inteface.run()
        db.insertData(db.dataFromFirebase)
        db.dataFromFirebase = []
        self.age_btn.values = self.getAge()                 
        self.gender_btn.values = self.getGender() 
        self.nativespeaker_btn.values = self.getNativeSpeaker()                          
        self.voiceid_btn.values = self.getVoice()   

    def getAge(self):
        """
        The method is to get the value for age from database that would be shown for options of Spinner
        
        Returns:
        list: The value of age
        """  
        column = "Age"
        c.execute("SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin ORDER BY " + column + " ASC")
        self.GetAge.insertData(c.fetchall())
        return self.GetAge.value()

    def getGender(self):
        """
        The method is to get the value for gender from database that would be shown for options of Spinner
        
        Returns:
        list: The value of gender
        """  
        column = "Gender"
        c.execute("SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin")
        self.GetGender.insertData(c.fetchall())
        return self.GetGender.value()

    def getNativeSpeaker(self):
        """
        The method is to get the value for nativeSpeaker from database that would be shown for options of Spinner
        
        Returns:
        list: The value of nativeSpeaker
        """  
        column = "NativeSpeaker"
        c.execute("SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin")        
        self.GetNativeSpeaker.insertData(c.fetchall())
        return self.GetNativeSpeaker.value()
    
    def getVoice(self):
        """
        The method is to get the value for voice from database that would be shown for options of Spinner
        
        Returns:
        list: The value of voice
        """  
        column = "VoiceId"
        c.execute("SELECT DISTINCT Voice FROM VoiceTable WHERE VoiceId IN (SELECT DISTINCT " + column + " FROM CrowdSourcingMandarin)")        
        self.GetVoice.insertData(c.fetchall())
        return self.GetVoice.value()

class Fetch():
    """
    The class is written to fetch the information easily
    """ 
    def __init__(self, column, extraData = None):
        """
        This method initialize the instances of Fetch.
        
        Parameters:
        column(string): the name of the column
        extraData(string): the extraData that is not from firebase
        """   
        self.extraData = extraData
        self.column = column
        self.data = []
        self.valueSelected = ''
    
    def insertData(self, data):
        """
        This method insert data into the self.data
        
        Parameters:
        data(list or string): the data selected from Spinner Options
        """   
        self.data = data
    
    def value(self):
        """
        This method is to return the value for Spinner Options
        
        Return:
        list: the list of data to be displayed for Spinner Options
        """   
        returnData = []
        for value in self.data:
            returnData.append(str(value[0]))
        if self.extraData is not None:
            returnData.append(self.extraData)
        print(returnData)
        return returnData
    
    def getColumn(self):
        """
        This method is to return the value of column
        
        Return:
        string: the name of the column
        """   
        return str(self.column)

    def getValue(self):
        """
        This method is to return the value of self.valueSelected
        
        Return:
        string: the selected value
        """   
        return str(self.valueSelected)
    
    def insertValue(self, value):
        """
        This method is to insert value into self.valueSelected
        
        Parameters:
        value(string): the value that is selected
        """   
        self.valueSelected = value
        

class Query():
    """
    The class is written to handle the query from databse
    """ 
    def __init__(self, obj, select, table, condition):
        """
        This method initialize the instances of Fetch.
        
        Parameters:
        obj(object): the object passed
        select(string): the information to be selected from table
        table(string): the name of table in database
        condition(string): the condition whether is All or All Commands
        """   
        self.column = obj.getColumn()
        self.value = obj.getValue()
        self.query = "SELECT " + select + " FROM " + table 
        if self.value != condition:
            self.query += " WHERE " + self.column + " = '" + self.value + "'"
    
    def getQuery(self):
        """
        This method is to return query for sqlite command
        
        Return:
        string: the query command
        """  
        return self.query
   
    def getValue(self):
        """
        This method is to return the value of self.value
        
        Return:
        string: the selected value
        """  
        return self.value

def toBeDownloaded(*argv):
    """
    This method is to trigger download of file based on the spinner option
    
    Parameters:
    *argv(object): accept the object passed
    """   
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
        dest = path_to_saved + parse_data["Age"] + "_" + parse_data["Gender"] + "_" + \
            parse_data["NativeSpeaker"] + "_" + parse_data["Command"]
        if (not os.path.exists(dest)):  
            os.makedirs(dest)
        for path in parse_data['Path']:
	        shutil.copyfile(path[0], dest + "\\" + path[0].split("\\")[-1]) 
    
class Alert(Popup):
    """
    The class is written to create alert when the input is invalid
    
    Parameters:
    PopUp(Inheritance of class): To inherit the class of PopUp from kivy.uix.popup
    """ 
    def __init__(self, title, text):
        """
        This method initialize the instances of Alert.
        
        Parameters:
        title(string): title of popup to be shown
        text(string): text of popup to be shown
        """   
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
