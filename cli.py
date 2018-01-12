import click
from utils import *

# @click.command()
# @click.option('--count', default = 1, help='Number of greetings.')
# @click.option('--name', prompt = 'Your name', help = 'The person to greet.')
# def hello(count, name):
#     for x in range(count):
#         click.echo('Hello %s!' % name)

# if __name__ == '__main__':
#     hello()

def createUser():
    header()
    click.echo("Create User")
    name = click.prompt("Name or Identifier", confirmation_prompt = True)
    user = create(name, testing = SETTINGS['debug'])
    header()
    click.echo("Your user ID: {}".format(user.getLogin()))
    click.echo("Your pin: {}".format(user.genPin()))
    click.echo("Keep this safe and don't tell anyone. Shhh.")
    click.prompt('', default='Press Enter/Return to continue')
    userMenu(user)

def loginScreen():
    header()
    click.echo("Login")
    user = login(click.prompt('User ID', type = str), click.prompt('PIN', type = str, hide_input = True))
    if user:
        userMenu(user)
    else:
        mainMenu(error = 'Failed to login. Try again.')

def seeChecklists():
    header()
    click.echo("See My Checklists")

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
    options = {'1' : ('Create User',createUser),
               '2' : ('Login', loginScreen)}
    createOptions(options)

def userMenu(user):
    header()
    click.echo('Welcome, {}'.format(user.getName()))
    options = {'1' : ('Logout', mainMenu)}
    createOptions(options, ET = userMenu, EM = None, params = {'user' : user})

@click.command()
@click.option('--debug', default = False, help='Debug options set such as testing documents.')
def main(debug):
    SETTINGS['debug'] = debug
    mainMenu()

################
"""MENU UTILS"""
################
def createOptions(options, ET = mainMenu, EM = 'Invalid choice!', **params):
    click.echo('What do you want to do?')
    keys = list(options.keys())
    keys.sort()
    for option in keys:
        click.echo('{} - {}'.format(option, options[option][0]))
    options['exit'] = ('Exit', exitCLI)
    options['menu'] = ('Go to Main Menu', mainMenu)
    choice = click.prompt('Choose an option', type = str)
    if choice not in options.keys():
        ET(params, error = EM)
    else:
        options[choice][1]()

SETTINGS = {}

if __name__ == '__main__':
    main()