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
    context.db_fd, meterage.app.config['DATABASE'] = tempfile.mkstemp()
    meterage.app.config['TESTING'] = True
    context.app = meterage.app.test_client()
    meterage.init_db()

    # add comments to the temporary database under each title
    # Note that an admin and a normal user are added.
    with closing(meterage.connect_db()) as db:
        g.db.execute('insert into comments (comment_input, entry_id, username) values (?,?,?)',
                 [request.form['comment_input'], entry_id, session['username']])
        
        db.commit()	
def after_all(context):
    """
    Close temporary file and remove from filesystem
    """
    os.close(context.db_fd)
    os.unlink(meterage.app.config['DATABASE'])