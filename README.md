# Ticketer

A ticket tracking system on a discord bot using a SQL database.

### database
database.py is a database manager i made that contains a `table` with "ticket" `elements` containing:
`id : int, date/time : str, context : str, author : str, solvedState : bool `
The way to refer to specific element in the database is by fetching the id for the element.

### ticket class

Tickets.py is a OOP class made to easily manage database entries.
this is mostly used to create and modify data in entries.

### discord bot
bot.py is one of the ways to manage and modify the database and functions as a user interface for the Ticket Tracking System,
it's a discord bot with commands and utility to add, modify and remove elements in the database.

some of the commands are:

.reset_data 
.submit
.remove
.entries
