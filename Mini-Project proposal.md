# Title

Crowd Sourcing Server For Mandarin 

# Team Jarvis

Members:

1. Choi Kai Sheng (kaishengchoi)
2. Lee Pin Loon (pllee4)
3. Teh Yee Bryan (bryteh)

# Overview

  In this project, we are trying to develop a server to collect voice of particular words like up, down, left, right, on, off, go, stop, numbers, etc. in mandarin. The database created will arrange the voice based on several characteristics and criteria such as gender, age, and command.The voice that collected though this crowdsourcing server is to be used in training of Artificial Neural Network model for speech recognition which will be applied in various application such as voice user interfaces (wheel chair control for disabled people and embedded system voice control), speech-to-text processing and etc.

  For this project, a local server will store all database of voice and its related information such as gender, age, native. The code for this server will be developed in Python Language. As for the mobile application side, Android Studio is used as IDE for code development. The code for this part will be written in Java Language. The voice collected from mobile application will be send to firebase storage as temporary storage. Local server will consistanly check for the availability of voice files in firebase storage and pull to local storage. The User Interface allow user to pull the needed voices with certain attribute from local storage.

# System Architecture

![architecture](https://github.com/kaishengchoi/fluffy-palm-tree/blob/master/SystemArchitecture.PNG)


# Class Diagram

![Class Diagram](https://github.com/kaishengchoi/fluffy-palm-tree/blob/master/softvoicecrowdsourcing.jpeg)


# Domain Model

![Domain model](https://user-images.githubusercontent.com/42335542/67346755-5c973100-f572-11e9-8497-2935be5af4a4.jpg)


# Entity-relationship Diagram

![erd](https://user-images.githubusercontent.com/42335542/67283801-ed382780-f506-11e9-9f85-fec9bdd6e55c.PNG)


# Database tables

* The messaging protocol we use is MQTT (machine-to-machine) connectivity protocol.
* The broker that we choose is cloudmqtt, it requires username and password for authentification
* The client would publish the data through the broker
* Raspberry Pi would subscribe to the topic to retrieve the data and store in local database using sqlite3
* The table created in database would be consisted of gender, age, command and voice.

Database structure: 

![Database1](https://user-images.githubusercontent.com/42335542/67276681-ccb4a100-f4f7-11e9-8ed2-57773956472b.png)

Some data in database:

![Database2](https://user-images.githubusercontent.com/42335542/67276931-464c8f00-f4f8-11e9-952d-74c434a1b4ea.png)

                                              

# User interface

The code for user interface for this project in written in python and Kivy open source python library. For more information on Kivy please refer to [Kivy's website](https://kivy.org/#home).

The image below shows the developed UI for this project.

![UI](https://github.com/kaishengchoi/fluffy-palm-tree/blob/master/UI.PNG)


# Website where Django server is based

This didn't use Django server, instead we are using SQLite as local database.

