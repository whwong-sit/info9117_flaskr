from behave import *
# import meterage

#### GIVENS


#### WHENS

@when(u'the User clicks "Gravatar settings"')
def step_impl(context):
    """
    Check that "Gravatar settings" is on this page, and then follow the link
    """
    assert "Gravatar settings" in context.rv.get_data(), '"Gravatar settings" is not on the current page'

    context.rv = context.app.get('/users/<username>/gravatar_settings')
    assert context.rv.status_code != 404, "Gravatar settings page does not exist"

@when(u'the User removes their Gravatar assignment')
def step_impl(context):
    raise NotImplementedError(u'Trying to implement this step would be too speculative at the current point, '
                              u'since we have not even got the web interface yet.  A likely idea would be that '
                              u'the userPassword table has the username, password, gravataremail and a Boolean '
                              u'for whether or not the user wants their Gravatar displayed.' )

#### THENS

@then(u'the Gravatar is displayed alongside the post')
def step_impl(context):
    assert '<li><h2><i><img src=' \
           '"http://www.gravatar.com/avatar/e6ac8cca83859e728591ef621ff6e9c4?s=50&amp;' \
           'd=monsterid"></i><br>&lt;Hello&gt; <span class=user> by hari </span>' in context.rv.get_data(), "image" \
                                                                                                            "is not" \
                                                                                                            "being dis" \
                                                                                                            "played"

@then(u'their Gravatar is not longer displayed beside posts')
def step_impl(context):
    assert '<li><h2><i><img src=' \
           '"http://www.gravatar.com/avatar/e6ac8cca83859e728591ef621ff6e9c4?s=50&amp;' \
           'd=monsterid"></i>' not in context.rv.get_data(), "image is still being displayed"
