import os
import meterage
import tempfile
from contextlib import closing


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

    names = ["admin", "hari"]
    passwords = ["default", "seldon"]
    emails = ["admin@unix.org", "hari@stroustrup.com"]

    # add users to the temporary database
    # Note that an admin and a normal user are added.
    with closing(meterage.connect_db()) as db:
        for name, password, email in zip(names, passwords, emails):
            db.execute('insert into userPassword (username, password, gravataremail) values (?, ?, ?)',
                       [name, password, email])
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

