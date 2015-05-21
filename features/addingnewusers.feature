Feature: As an Administrator, I want the ability to add new users or for users to add themselves and only really be added upon my approval

  Scenario: User register for login
    Given the user goes to register page
    When the user register
    Then registration performed successfully

  Scenario: Admin add new user
    Given the Admin is logged in
	When the Admin goes to adding_new_user page
	And the Admin add new user for login
	Then Admin adding new user performed successfully

  Scenario:user login and the account with admins approval
	Given admin has approved a new user
	When the user is logged in
	Then the user login successfully
	

  Scenario:user login and the account without admins approval
	Given a user registration without permission
	When the user is logged in	
	Then the user login fails