from models import *

##############
"""FUNTIONS"""
##############
def login(userID, pin):
    user = getUser(findUser(userID))
    if user:
        if user.checkPin(pin):
            return user
        else:
            return None
    else:
        return None

def createUser(name, testing = False, admin = False):
    user = User(name, testing = testing, admin = admin)
    addUser(user)
    return user

def createChecklist(name, testing = False):
    cl = Checklist(name, testing = testing)
    addChecklist(cl)
    return cl

def createChecklistItem(itemId, specs, testing = False):
    cli = ChecklistItem(itemId, specs, testing = testing)
    addChecklistItem(cli)
    return cli

def createItem(name, categoryId, testing = False):
    item = Item(name, categoryId, testing = testing)
    addItem(item)
    return item

def createCategory(name, attributes, testing = False):
    category = Category(name, attributes, testing = testing)
    addCategory(category)
    return category
