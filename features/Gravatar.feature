# Analysis:
# There should be a mapping from username to Gravatar image
#
# Design Sketch:
# Gravatar image for <user> should be displayed with every post for <user
#
# The Gravatar image should be "assigned" to the account, i.e. it should
# map to the unique identifier of an account, the username

Feature: Gravatar image
  As a User, I want to assign a Gravatar image to my account.

  Scenario: Making a post
    Given the User is logged in
    When the User makes a post
    Then the Gravatar is displayed alongside the post

  Scenario: Managing my details
    Given the User is logged in
    When the User navigates to the web interface
    Then the User is able to edit and commit Gravatar email
    # note that this "Then" is covered in UserAccountWebInterface.feature

  Scenario: Removing my Gravatar assignment
    Given the User is logged in
    When the User makes a post
    And the User removes their Gravatar assignment
    Then their Gravatar is no longer displayed beside posts
