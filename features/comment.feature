Feature: comment

  Scenario: post comment
     Given the user is logged in
     When create a entry
     And click add_comment
     Then the comment should appear