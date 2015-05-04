Feature: startandendtime

  Scenario: create start time
     Given the user is logged in
     When create a entry
     Then start time will auto_sign

  Scenario: create end_time
     Given the user is logged in
     When create a entry
     And press end_task
     Then end time should auto_sign