Feature: startandendtime

  Scenario: create start time
     Given the user has logged in already
     When the user add a new entry to log
     Then start time will auto_sign

  Scenario: create end_time
     Given the user has logged in already
     When the user press end_task
     Then end time should auto_sign