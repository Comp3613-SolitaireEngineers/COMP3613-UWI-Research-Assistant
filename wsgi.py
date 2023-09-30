import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *
from datetime import datetime

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Admin Commands
'''

user_cli = AppGroup('admin', help='Admin object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates an admin")
@click.argument("admin_id", default="strid")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def create_admin_command(admin_id, username, password):
    create_admin(admin_id, username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

'''
Publcations Commands
'''
publication_cli = AppGroup('publication', help='publication object commands')

@publication_cli.command('create', help='List all authors')
def create_publication_command():
    title = click.prompt("Enter title ", type = str)
    author_id = click.prompt("Enter author id ", type = str)
    publication_date = datetime.now() #click.prompt("Enter publication date", type = str)
    publication = create_publication(title, publication_date, author_id)
    
    if publication:
        print(f"Publication: - {publication}")
    else:
        print("Publocation not created.")
        
@publication_cli.command('author_publications', help="List all author's publications")
def list_publications_by_author_command():
    author_id = click.prompt("Enter author ID ", type = str)
    publications = get_publications_by_author(author_id)
    if publications:
        print("Publications:")       
        print(f"- {publications})")
    else:
        print("No publications found.")    

app.cli.add_command(publication_cli) 

