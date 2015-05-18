Feature: Start and End Time

  Scenario: Create Start Time
     Given the user has logged in already
     When the user add a new entry to log
     Then start time will auto sign

  Scenario: Create End Time
     Given the user has logged in already
     When the user presses end_task
     Then end time should auto sign
