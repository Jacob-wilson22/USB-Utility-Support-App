**USB Utility Support App Documentation**

Overview: A modelled solution to improve on the current device checking system in place at the Urban Science Building (USB)

To run the application edit the configuration so it runs through the app file.

To successfully run this application the following python libraries will have to be installed:

flask
flask-login
flask-WTF
wtforms
wtforms.validators
werkzeug.security
plotly.graph_objs
plotly.utils
datetime
sql-alchemy 
sql-alchemy.orm

**Data Folder**

Rooms.csv: Contains data regarding rooms within the USB.

Devices.csv: Contains data regarding devices within the USB.

Faults.csv: Contains data regarding the faults a device checker is expected to encounter.

**Python Files**

app.py: This file contains the application configurations, creates the database instance and registers all of the application blueprints written in the views.py file.

Config.py: Stores database config details.

views.py: This file stores all the blueprint routes for the application.

forms.py: This file stores the structure of all the forms used within the application.

query.py: This file stores all of the sql queries utilised within the blueprints in the views.py file. 

models.py:  This file defines the structure of all the tables within the application database. 

populate.py: Populates relevant database tables with the csv files from the data folder. 


**HTML Files**

Base.html: Contains all the consistent styling for the application as well as lines of code for the applications navbar. 

Homepage.hmtl: Responsible for displaying the homepage content which acts as a connector between all the applications features.  

Floors.html: This html is responsible for displaying all the floors the user can select when reporting a device. 

Rooms.html: This html is responsible for displaying all the rooms the user can select when reporting a device. 

Devices.html: This html is responsible for displaying all the devices the user can select when reporting a device. This html also stores the device log form, which users can use to report a device.

Fault_log.html: This html displays the contents of the Fault_log table to the user within a table.

Graphs.html: This html displays fields from the fault_log table as visual insights for the user. 

Register.html: Stores the register form allowing users to register an account for the application. 

Login.html: Stores the login form allowing users with credentials to access the application.

Tasks.html: Acts a homepage for task management. With a button to access the task assignment functionality and a button to access task view functionality. 

Task_assign.html: Allows admin users to assign tasks to all users registered to the application.

Task_view.html: Allows all users to see all tasks assigned and their deadlines. 



