Feature: Start and End Time

  Scenario: Create Start Time
     Given the User is logged in
     When the user adds a new entry to log with an unspecified start time
     Then start time will auto sign

  Scenario: Create End Time
     Given the User is logged in
     When the user presses end_task
     Then end time will auto sign
