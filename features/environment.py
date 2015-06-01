import os
import meterage
import tempfile
from contextlib import closing

from flask_bcrypt import check_password_hash

from models import User

# These run before and after every step.
def before_step(context, step):
    pass


def after_step(context, step):
    pass


# These run before and after each scenario is run.
def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    pass


# These run before and after each feature file is exercised.
def before_feature(context, feature):
    """
    Create a new test client, initialise a database and activate TESTING mode
    """
    context.db_fd, meterage.app.config['DATABASE'] = tempfile.mkstemp()
    meterage.app.config['TESTING'] = True
    context.app = meterage.app.test_client()
    meterage.init_db()

    #flat dictionary of users, so we have access to the plain text versions of the passwords
    context.users = {"admin": "default", "hari": "seldon"}

    # add users to the temporary database
    # Note that an admin and a normal user are added.
    with closing(meterage.connect_db()) as db:
        admin = User('admin', 'default', 'admin@unix.org', True, True)
        db.execute('insert into userPassword (username, password, gravataremail,flag_admin,flag_approval) values (?, ?, ? ,? ,?)',
                   [admin.username, admin.password, admin.gravataremail, admin.flag_admin, admin.flag_approval])
        user = User('hari', 'seldon', 'hari@stroustrup.com', False, True)
        db.execute('insert into userPassword (username, password, gravataremail,flag_admin,flag_approval) values (?, ?, ?,? ,?)',
                   [user.username, user.password, user.gravataremail, user.flag_admin, user.flag_approval])
        user2 = User('spock', 'vulcan', 'livelong@prosper.edu.au', True, True)
        db.execute('insert into userPassword (username, password, gravataremail,flag_admin,flag_approval) values (?, ?, ?,? ,?)',
                   [user2.username, user2.password, user2.gravataremail, user2.flag_admin, user2.flag_approval])
        user3 = User('test', 'test', 'test@test.edu.au', False, True)
        db.execute('insert into userPassword (username, password, gravataremail,flag_admin,flag_approval) values (?, ?, ?,? ,?)',
                   [user3.username, user3.password, user3.gravataremail, user3.flag_admin, user3.flag_approval])
        db.commit()


def after_feature(context, feature):
    """
    Close temporary file and remove from filesystem
    """
    os.close(context.db_fd)
    os.unlink(meterage.app.config['DATABASE'])


# These run before and after a section tagged with the given name. They are invoked
# for each tag encountered in the order they’re found in the feature file.
def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass


# These run before and after the whole shooting match.
def before_all(context):
    pass

def after_all(context):
    pass


def after_all(context):
    pass

