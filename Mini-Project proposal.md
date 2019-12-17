# Title

Crowd Sourcing Server For Mandarin 

# Team Jarvis

Members:

1. Choi Kai Sheng (kaishengchoi)
2. Lee Pin Loon (pllee4)
3. Teh Yee Bryan (bryteh)

# Overview

  In this project, we are trying to develop a server to collect voice of particular words
like up, down, left, right, on, off, go, stop, numbers, etc. in mandarin. The database 
created will arrange the voice based on several characteristics and criteria such as gender,
age, and command.The voice that collected though this crowdsourcing server is to be used in
training of Artificial Neural Network model for speech recognition which will be applied in
various application such as voice user interfaces (wheel chair control for disabled people and
embedded system voice control), speech-to-text processing and etc.

  For this project, a Raspberry Pi will be use as local server to store all database of voice.
The code for this server will be developed in Python Language. As for the mobile application 
side, Android Studio will be use as IDE for code development. The code for this part will be 
written in Java Language. The voice collected from mobile application will be send to server
though MQTT protocol.

# System Architecture


![architecture](https://user-images.githubusercontent.com/42335542/67276010-5e231380-f4f6-11e9-811c-bdde78474ab4.png)

[MQTT protocol is explained here](https://user-images.githubusercontent.com/42335542/67277334-28cbf500-f4f9-11e9-8b68-f364a8bbd676.png)

# Class Diagram

[Link for Class Diagram](https://github.com/pllee4/Jarvis/blob/master/Class%20diagram.md)

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



# Website where Django server is based

  Since our project does not use website, we do not use Django, the borker website used for MQTT is soldier.mqtt.com
