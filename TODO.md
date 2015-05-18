* Make usernames unique.  If a user changes their username to another
  user's username, or even worse changes it to "admin", then
  everything goes haywire.

* Change the implementation for being an "admin".  It should be a
  Boolean value in the userPassword table.

* Make everything much prettier.

* Distribute the main meterage.py across multiple files, it is getting
  too large