import os
import flaskr
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
    pass


def after_feature(context, feature):
    pass


# These run before and after a section tagged with the given name. They are invoked
# for each tag encountered in the order they’re found in the feature file.
def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass
	

# These run before and after the whole shooting match.
def before_all(context):
    """
    Create a comments for title, initialise a database and activate TESTING mode
    """
    context.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    context.app = flaskr.app.test_client()
    flaskr.init_db()

    # add comments to the temporary database under each title
    # Note that an admin and a normal user are added.

def after_all(context):
    """
    Close temporary file and remove from filesystem
    """
    os.close(context.db_fd)
    os.unlink(flaskr.app.config['DATABASE'])