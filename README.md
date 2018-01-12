#CHECK
##A Customizable Checklist App
Currently Developed For: Command Line Interface

##Set-Up
In order for the application to work you must have a 'db.py' file located in the Checklist directory. This file should connect you to a database. Currently, the application is set up for 5 tables/collections (`users`, `checklists`, `checklistItems`, `items`, `categories`). Your database should be set up to handle these 5 tables/collections.

You must have a variable for each of the tables/collections above (use the same name as indicated above). Finally you must have 5 functions:

`updateC(table, object)`
    `table`  : table/collection variable
    `object` : class object for given type
    purpose  : updates the corresponding object in the database 
    returns  : None

`getC(table, id)`
    `table`  : table/collection variable
    `id`     : object's id
    returns  : dictionary form of class object

`addC(table, object)`
    `table`  : table/collection variable
    `object` : class object for given type
    purpose  : adds new object to table/collection in the database 
    returns  : Database's object id

`clearTests()`
    purpose  : Deletes all entries in the databse with the attribute `testing = False`

`findUser(userID)`
    `userID` : 6-digit login id for a user
    returns  : class object id for the user

####Example (MongoDB - pymongo):
```
import pymongo as pm

#localhost
client = pm.MongoClient()

#checklist databse
db = client['checklist']

categories = db['categories']
items = db['items']
checklistItems = db['checklistItems']
checklists = db['checklists']
users = db['users']

def updateC(collection, obj):
    return collection.update({'id':obj.getId()}, vars(obj))

def getC(collection, id):
    return collection.find_one({"id" : id})

def addC(collection, obj):
    return collection.insert(vars(obj))

def clearTests(db):
    for collection in db.collection_names():
        print(db[collection].remove({'testing' : True}))

def findUser(userID):
    return users.find_one({'login':userID})['id']
```

##To Start
Install the necessary packages
`pip install -r requirements.txt`

Run the cli program
`python3 cli.py`