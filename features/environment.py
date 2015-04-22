# These run before and after every step.
def before_step(context, step):
    pass


def after_step(context, step):
    pass


# These run before and after the whole shooting match.
def before_all(context):
    pass


def after_all(context):
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
