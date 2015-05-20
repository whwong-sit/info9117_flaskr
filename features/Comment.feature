Feature: Write comment for entries

  Scenario: add a new comment to new entries
     Given the User is logged in
     When the User makes a post
     And click the entry, the user would be able to add a comment each time
     Then the comment should appear right after added
     And the username should displayed right next to the comment

  Scenario: add a new comment to existing entries
     Given the User is logged in
     When click the entry, the user would be able to add a comment each time
     Then the comment should appear right after added
     And the username should displayed right next to the comment

  