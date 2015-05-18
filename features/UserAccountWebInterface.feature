# Analysis:
#  If you want to "manage details" then this means you want to be able to view
#  these details and edit (at least some of) them.
#
# Design Sketch:
#  * A button/link on the main page to be taken to a "manage details" page.
#  * The page should display username and any other details associated with that username
#  * The option to change password should be available, as well as other details

Feature: User account web interface
  As a User, I want to manage details of
  my accounts through a web interface.

  Scenario: View current details
    Given the User is logged in
    When the User navigates to the web interface
    Then account details are displayed

  Scenario Outline: Edit details
    Given the User is logged in
    When the User navigates to the web interface
    Then the User is able to edit and commit <detail>
  Examples:
    | detail         |
    | username       |
    | Gravatar email |
