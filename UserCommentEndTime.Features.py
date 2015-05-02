# Analysis:
#  If you want to "add comments" then this means you want to be able to view
#  these comments.
#
# Design Sketch:
#  * A link on the main page to be taken to a "comments" html page.
#  * The page should display the tile under which it is commenting and by which username
#  * The page also displays start_time by default and when the end-task button is pressed the actual end_time would be displayed   
#  * The page should display comment text area and any other details associated with that username
#  * Other users could also comment on the topics posted by others if they are logged in.

Feature: Comments being displayed under each title in a new web interface
         Other users are also available to comment in post in
 
  Scenario: View comments under each title
    If the User is logged in
    When the User navigates to the  comments web interface
    Then comments are displayed under each title topics.

  Scenario Outline: Insert Comments under Title
    If the User is logged in
    When the User navigates to the comments web interface
    And the User clicks "Title" it goes to a different web interface(comments.html).
    Then the User is able to Comment under each title

  Examples:
    | Title  |
    | username |
	| start_time |
	| end_time |
    | Comments |