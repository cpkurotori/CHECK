from models import *

##############
"""FUNTIONS"""
##############
def login(userID, pin):
    try:
        id = findUser(userID)
    except:
        return None
    user = getUser(id)
    if user:
        if user.checkPin(pin):
            return user
        else:
            return None
    else:
        return None

def create(name, testing = False):
    user = User(name, testing = testing)
    addUser(user)
    return user

