from uuid import uuid4 as id_gen
from random import randint as ri
from db import *
import bcrypt

class InvalidAttributeError(Exception):
    def __repr__(self):
        return 'Attribute is not valid'

    def __str__(self):
        return repr(self)

class OverrideError(Exception):
    def __repr__(self):
        return 'There is already a value for given attribute. Override required.'

    def __str__(self):
        return repr(self)

class PinError(Exception):
    def __repr__(self):
        return 'A pin is required for the user.'

    def __str__(self):
        return repr(self)

class Category:
    def __init__(self, name, attributes, 
                id = str(id_gen()), testing = False, **kwargs):
        self.name = name
        self.attributes = attributes
        self.id = id
        if testing:
            self.testing = testing

    def getName(self):
        return self.name

    def getAttributes(self):
        return self.attributes

    def getId(self):
        return self.id

    def __repr__(self):
        return "[Category] : {}\n  [Attributes] : {}".format(self.name, self.attributes)

    def __str__(self):
        return repr(self)

class Item:
    def __init__(self, name, categoryId, id = None, 
                testing = False, **kwargs):
        self.name = name
        self.categoryId = categoryId
        self.id = id
        if testing:
            self.testing = testing

    def getName(self):
        return self.name

    def getCategoryId(self):
        return self.categoryId

    def getId(self):
        return self.id

    def __repr__(self):
        return "[Item] : {}\n  [Category] : {}".format(self.name, getCategory(self.categoryId).getName())

    def __str__(self):
        return repr(self)

class ChecklistItem:
    def __init__(self, itemId, id = str(id_gen()), 
                specs = {}, testing = False, **kwargs):
        self.itemId = itemId
        self.id = id
        self.specs = specs
        if testing:
            self.testing = testing
        item = getItem(itemId)
        category = getCategory(item.getCategoryId())
        if not specs:
            for attr in category.getAttributes():
                self.specs[attr] = None

    def setSpec(self, attr, value, override = False, 
                id = str(id_gen()), testing = False, **kwargs):
        if attr not in getCategory(getItem(self.itemId).getCategoryId()).getAttributes():
            raise InvalidAttributeError
        elif self.specs[attr] is not None and not override:
            raise OverrideError
        else:
            self.specs[attr] = value
        updateChecklistItem(self)

    def getItemId(self):
        return self.itemId

    def getSpecs(self):
        return self.specs

    def getId(self):
        return self.id

    def __repr__(self):
        return "[ChecklistItem]:\n  [Specs] : {}".format(self.specs)

    def __str__(self):
        return repr(self)

class Checklist:
    def __init__(self, name, id = str(id_gen()), 
                items = [], testing = False, **kwargs):
        self.name = name
        self.id = id
        self.items = items
        if testing:
            self.testing = testing

    def addItem(self, chklstItmId):
        self.items.append(chklstItmId)
        updateChecklist(self)

    def getName(self):
        return self.name

    def getItems(self):
        return self.items

    def getId(self):
        return self.id

    def __repr__(self):
        return "[Checklist] : {}\n  [Items] : {}".format(self.name, [getItem(getChecklistItem(itemId).getItemId()).getName() for itemId in self.items])

    def __str__(self):
        return repr(self)

class User:
    def __init__(self, name, id = str(id_gen()), 
                login = ''.join(map(str,[ri(0,9) for _ in range(6)])), 
                pin = None, checklists = {}, testing = False, **kwargs):
        self.name = name
        self.checklists = checklists
        self.id = id
        self.login = login
        #print(self.login)
        self.pin = pin
        if testing:
            self.testing = testing

    def pin_required(f):
        def wrapper(self, *args):
            if self.pin is None:
                raise PinError
            else:
                return f(self, *args)
        return wrapper

    @pin_required
    def addChecklist(self, chklstId):
        checked = {}
        checklist = getChecklist(chklstId)
        for itemId in checklist.getItems():
            checked[itemId] = False
        self.checklists[chklstId] = checked
        updateUser(self)

    def genPin(self):
        pin = ''.join(map(str,[ri(0,9) for _ in range(4)])).encode()
        self.pin = bcrypt.hashpw(pin, bcrypt.gensalt())
        updateUser(self)
        return pin.decode()

    def checkPin(self, pin):
        return bcrypt.hashpw(pin.encode(), self.pin) == self.pin

    def getName(self):
        return self.name

    def getChecklists(self):
        return self.checklists

    def getId(self):
        return self.id

    def getLogin(self):
        return self.login

    def __repr__(self):
        return "[User] : {}\n  [Checked] : {}".format(self.name, self.checklists)

    def __str__(self):
        return repr(self)


##########
"""GETS"""
##########
def getCategory(id):
    try:
        return Category(**getC(categories, id))
    except:
        return None

def getItem(id):
    try:
        return Item(**getC(items, id))
    except:
        return None

def getChecklistItem(id):
    try:
        return ChecklistItem(**getC(checklistItems, id))
    except:
        return None

def getChecklist(id):
    try:
        return Checklist(**getC(checklists, id))
    except:
        return None

def getUser(id):
    try:
        return User(**getC(users, id))
    except:
        return None

##########
"""ADDS"""
##########
def addCategory(obj):
    #print("adding category")
    return addC(categories, obj)

def addItem(obj):
    #print("adding item")
    return addC(items, obj)

def addChecklistItem(obj):
    #print("adding checklist item")
    return addC(checklistItems, obj)

def addChecklist(obj):
    #print("adding checklist")
    return addC(checklists, obj)

def addUser(obj):
    #print("adding user")
    return addC(users, obj)

#############
"""UPDATES"""
#############
def updateCategory(obj):
    #print("adding category")
    return updateC(categories, obj)

def updateItem(obj):
    #print("adding item")
    return updateC(items, obj)

def updateChecklistItem(obj):
    #print("adding checklist item")
    return updateC(checklistItems, obj)

def updateChecklist(obj):
    #print("adding checklist")
    return updateC(checklists, obj)

def updateUser(obj):
    #print("adding user")
    return updateC(users, obj)
