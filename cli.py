import click
from utils import *

class Option:
    def __init__(self, function, desc, params = {}):
        self.function = function
        self.desc = desc
        self.params = params

    def __call__(self):
        return self.function(**self.params)

    def __str__(self):
        return self.desc

def createUser():
    header()
    click.echo("Create User")
    name = click.prompt("Name or Identifier", confirmation_prompt = True)
    user = createU(name, testing = SETTINGS['debug'])
    header()
    click.echo("Your user ID: {}".format(user.genLogin()))
    click.echo("Your pin: {}".format(user.genPin()))
    click.echo("Keep this safe and don't tell anyone. Shhh.")
    pause()
    userMenu(user)

def createChecklist():
    header()
    center("Create Checklist")
    createCL(click.prompt("Checklist Name"), testing = SETTINGS['debug'])
    manageMenu()

def loginScreen():
    header()
    click.echo("Login")
    user = login(click.prompt('User ID', type = str), click.prompt('PIN', type = str, hide_input = True))
    if user:
        userMenu(user)
    else:
        mainMenu(error = 'Failed to login. Try again.')

def viewChecklists():
    header()

def seeChecklists(user):
    header()
    click.echo("See My Checklists")
    pause()
    userMenu(user)


def exitCLI(*args, **kargs):
    click.clear()
    click.echo("Goodbye.")
    quit()

def header():
    click.clear()
    centerH('Hello, World!', fg='green')
    centerH('Welcome to', fg='blue')
    centerH('CHECK', fg='red', bold=True)
    click.echo()
    click.echo()

def centerH(text, **styles):
    width, height = click.get_terminal_size()
    spaces = ' '*(width//2-len(text)//2)
    click.secho(spaces+text+spaces, **styles)



#############
""" MENUS """
#############

def mainMenu(error = None, *args, **kargs):
    header()
    if error:
        click.secho(error, fg='red')
    options = {'1' : Option(createUser, 'Create User'),
               '2' : Option(loginScreen, 'Login'),
               '3' : Option(manageMenu, 'Checklist Management')}
    createOptions(options)

def userMenu(user):
    header()
    click.echo('Welcome, {}'.format(user.getName()))
    options = {'1' : Option(mainMenu, 'Logout'),
               '2' : Option(seeChecklists, 'My Checklists', {'user' : user})}
    createOptions(options, ET = userMenu, params = {'user' : user})

def manageMenu():
    header()
    options = {'1' : Option(createChecklist, 'Create new Checklist'),
               '2' : Option(viewChecklists, 'View/Modify Checklists')}
    createOptions(options, ET = manageMenu, EM = None)



@click.command()
@click.option('--debug', default = False, help='Debug options set such as testing documents.')
def main(debug):
    SETTINGS['debug'] = debug
    mainMenu()

################
"""MENU UTILS"""
################
def createOptions(options, ET = mainMenu, params = {'error' : 'Invalid Choice!'}):
    click.echo('What do you want to do?')
    keys = list(options.keys())
    keys.sort()
    for option in keys:
        click.echo('{} - {}'.format(option, str(options[option])))
    options['exit'] = Option(exitCLI, 'Exit')
    options['menu'] = Option(mainMenu, 'Main Menu')
    choice = click.prompt('Choose an option', type = str)
    if choice not in options.keys():
        ET(**params)
    else:
        options[choice]()

def pause():
    click.prompt('', default='Press Enter/Return to continue')

SETTINGS = {}

if __name__ == '__main__':
    main()