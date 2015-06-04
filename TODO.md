# To Do

[x] Make usernames unique.  If a user changes their username to
    another user's username, or even worse changes it to "admin", then
    everything goes haywire.

[x] Change the implementation for being an "admin".  It should be a
    Boolean value in the userPassword table.

[ ] Make everything much prettier.

[x] Distribute the main meterage.py across multiple files, it is
    getting too large

[x] Fix up the database connections/disconnectons

[ ] Implement the Entry start_time and end_time fields to use DateTime
    objects.

[ ] Fix up the setUp and tearDown methods in the unit tests so they
    work correctly with SQLAlchemy

[ ] Refactor.  The code is getting unruly at this point.  In
    particular consolidate the methods for adding/approving new users

[ ] Implement email confirmations.  There is an official Flask
    extension to this end.
