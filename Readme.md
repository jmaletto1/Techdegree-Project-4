Unit-4 Techdegree Project

app.py completes the following functions in order to create a Store Inventory tool for a restuarant.

- Imports OrderedDict, csv, datetime, os, sys, decimal and peewee
- Creates a Database file using SqLiteDatabase
- Creates a Product class, and then cleans the data from the csv file
- The data from the CSV File is then stored in the database file
- The add_entry() function allows users to create an entry, or update an already existing item.
- The view_product() function helps users search for a product by it's id number. Error checks are in place in case the item does not exist.
- The user can create a backup csv file with the create_backup() function.
- Finally, the main menu allows the user to choose from the 3 main functions, as well as pressing 'q' to quit.

John Austen
