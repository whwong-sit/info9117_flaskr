Feature: Write comment for entries

  Scenario: add a new comment to new entries
     Given the user has logged in already
     When the user add a new entry to log
     And click the entry, the user would be able to add a comment each time
     Then the comment should appear right after added
     And the username should displayed right next to the comment

  Scenario: add a new comment to existing entries
     Given the user has logged in already
     When click the entry, the user would be able to add a comment each time
     Then the comment should appear right after added
     And the username should displayed right next to the comment

  