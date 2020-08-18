#!/usr/bin/env python3

from collections import OrderedDict
import csv
import datetime
import os
import sys

from decimal import Decimal
from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    product_name = CharField(unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db


def initialise():
    db.connect()
    db.create_tables([Product], safe=True)


def csv_pull():
    """Pull CSV Items and add to our Database"""
    with open('inventory.csv', newline='') as csvfile:
        info = csv.DictReader(csvfile)
        rows = list(info)
        for i in rows:
            try:
                Product.create(product_name=i['product_name'],
                               product_price=int(
                    round(float(i['product_price'].replace('$', '')) * 100)),
                    product_quantity=int(i['product_quantity']),
                    date_updated=datetime.datetime.today()
                )
            except IntegrityError:
                inv_item = Product.get(product_name=i['product_name'])
                inv_item.product_price = int(
                    round(float(i['product_price'].replace('$', '')) * 100))
                inv_item.product_quantity = int(i['product_quantity'])
                inv_item.date_updated = datetime.datetime.today()
                inv_item.save()


def add_entry():
    """Add a new Product to our database"""
    try:
        name = input("Product name: ")
        entry_price = input("Price: $")
        price = int(round(float(entry_price) * 100))
        quantity = int(input("Quantity: "))
        # date = date.datetime.today()
        if not name.isalpha():
            raise TypeError(
                "I'm afraid that is an invalid name for your product.")
    except TypeError:
        print("Oh nooz that didn't work!")
    print(f"Product name: {name}")
    print(f"Product price: ${entry_price}")
    print(f"Product quantity: {quantity}")
    confirmation = input(
        "Please confirm if you'd like to add this product to the inventory. y/n: \n")
    if confirmation.lower() == 'y':
        try:
            Product.create(
                product_name=name,
                product_price=price,
                product_quantity=quantity,
                date_updated=datetime.datetime.today()
            )
            print("Product successfully added!")
        except IntegrityError:
            inv_item = Product.get(product_name=name)
            inv_item.product_price = int(
                round(float(price)))
            inv_item.product_quantity = int(quantity)
            inv_item.date_updated = datetime.datetime.today()
            inv_item.save()
            print("Product successfully updated!")
    elif confirmation.lower() != 'y':
        print("Entry not added. Now returning you to the main menu.")


def view_product():
    """View an item from the inventory"""
    while True:
        try:
            view_id = input("Please enter the ID of an item: ")
            product = Product.get(Product.product_id == view_id)
            name = product.product_name
            price = (product.product_price / 100)
            quantity = product.product_quantity
            show_price = "{:.2f}".format(price)
            last_date = product.date_updated.strftime('%A %d %Y at %H:%M:%S')
            print(f"\n{name} is priced at ${show_price}")
            print(f"There are currently {quantity} item(s) in stock.")
            print(f"This item was last updated on {last_date}.")
        except DoesNotExist:
            print(
                "\nI'm afraid we cannot find that item. Please try again.")
            continue
        repeater = input("\nWould you like to view another product? y/n: ")
        if repeater.lower() == 'y':
            continue
        else:
            print("\nReturning you to the main menu!")
            break


def create_backup():
    """Create a backup of the Database, exported as a .CSV"""
    with open('backup_inventory.csv', 'w') as backup_file:
        fieldnames = ['product_id', 'product_name',
                      'product_price', 'product_quantity', 'date_updated']
        csv_writer = csv.DictWriter(backup_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for i in Product:
            csv_writer.writerow({
                "product_id": i.product_id,
                "product_name": i.product_name,
                "product_price": "${:.2f}".format(i.product_price / 100),
                "product_quantity": i.product_quantity,
                "date_updated": i.date_updated.strftime('%m/%d/%Y')
            })
        print("\nBackup successfully completed!")


def inventory_control():
    """Master Control Section"""
    menu = OrderedDict([
        ('a', add_entry),
        ('v', view_product),
        ('b', create_backup),
        # ('d', delete_entry),
    ])
    selection = None

    while selection != 'q':
        print("\nPlease select from the following options. Enter 'q' to quit\n")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))

        try:
            selection = input("\nSelection: ").lower().strip()
            if selection in menu:
                menu[selection]()

        except ValueError:
            print(
                "\nThat was an invalid selection. Please try again, or press 'q' to quit..")


if __name__ == '__main__':
    initialise()
    csv_pull()
    inventory_control()
