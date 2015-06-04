import os
import tempfile

import meterage


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
    meterage.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + meterage.app.config['DATABASE']
    meterage.app.config['TESTING'] = True

    # We cannot be in debug mode or Flask raises an AssertionError
    meterage.app.config['DEBUG'] = False

    # Make this true to see all of the SQL queries fly by in the console
    meterage.app.config['SQLALCHEMY_ECHO'] = False
    meterage.db = meterage.SQLAlchemy(meterage.app)
    reload(meterage.models)
    context.app = meterage.app.test_client()

    meterage.db.create_all()

    # flat dictionary of users, so we have access to the plain text versions of the passwords
    context.users = {"admin": "default", "hari": "seldon"}

    # add users to the temporary database
    # Note that an admin and a normal user are added.
    meterage.db.session.add(meterage.User('admin', 'default', 'admin@unix.org', True, True))
    meterage.db.session.add(meterage.User('hari', 'seldon', 'hari@stroustrup.com', False, True))
    meterage.db.session.add(meterage.User('spock', 'vulcan', 'livelong@prosper.edu.au', True, True))
    meterage.db.session.add(meterage.User('test', 'test', 'text@text.edu.au', False, True))    
    meterage.db.session.commit()


def after_feature(context, feature):
    """
    Close temporary file and remove from filesystem
    """
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
