import sqlite3
import json
from models import Animal
from models.customer import Customer
from models.location import Location


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            c.id customer_id,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email,
            l.id location_id,
            l.name location_name,
            l.address location_address
        FROM Animal a
        JOIN Customer c
            ON c.id = a.customer_id
        JOIN Location l
            ON l.id = a.location_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
    #     for row in dataset:

        for row in dataset:

            customer = Customer(row['id'],
                                row['customer_name'],
                                row['customer_address'],
                                row['customer_email']
                                )

        # Create a Location instance from the current row
            location = Location(row['id'],
                                row['location_name'],
                                row['location_address'])

        # Add the dictionary representation of the location to the animal
            # Create an animal instance from the current row
            animal = Animal(row['id'],
                            row['name'],
                            row['status'],
                            row['breed'],
                            row['customer_id'],
                            row['location_id'],
                            customer.__dict__,
                            location.__dict__
                            )

        # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return json.dumps(animals)


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id,
            c.id customer_id,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email,
            l.name location_name,
            l.address location_address
        FROM animal a
        JOIN customer c
            ON c.id = a.customer_id
        JOIN location l
            ON l.id = a.location_id
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        customer = Customer(data['customer_id'],
                            data['customer_name'],
                            data['customer_address'],
                            data['customer_email']
                            )

        location = Location(data['location_id'],
                            data['location_name'],
                            data['location_address']
                            )

        # Create an animal instance from the current row
        # Gets constructed from the __init__
        animal = Animal(data['id'],
                        data['name'],
                        data['status'],
                        data['breed'],
                        data['customer_id'],
                        data['location_id'],
                        location.__dict__,
                        customer.__dict__
                        )

        return json.dumps(animal.__dict__)


def get_animals_by_location_id(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
            FROM animal a
            WHERE a.location_id = ?
            """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'],
                row['name'],
                row['status'],
                row['breed'],
                row['customerId'],
                row['locationId']
            )
            animals.append(animal.__dict__)

    return json.dumps(animals)


def get_animals_by_status(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
            From animal a
            WHERE a.status = ?
            """, (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'],
                row['name'],
                row['status'],
                row['breed'],
                row['customer_id'],
                row['location_id']
            )
            animals.append(animal.__dict__)

    return json.dumps(animals)


def create_animal(new_animal):
    # new_animal is body sent from POST

    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal 
            (name,
            breed,
            status,
            location_id,
            customer_id
            )
        VALUES( ?, ?, ?, ?, ? );
        """, (
            new_animal['name'],
            new_animal['breed'],
            new_animal['status'],
            new_animal['locationId'],
            new_animal['customerId'],
        ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return json.dumps(new_animal)


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (
            new_animal['name'],
            new_animal['breed'],
            new_animal['status'],
            new_animal['locationId'],
            new_animal['customerId'],
            id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id= ?
        """, (id, ))


# ANIMALS = [
#     {
#         "id": 1,
#         "name": "Snickers",
#         "breed": "Dog",
#         "status": "Admitted",
#         "customer_id": 4,
#         "location_id": 1
#     },
#     {
#         "id": 2,
#         "name": "Gypsy",
#         "breed": "Dog",
#         "status": "Admitted",
#         "customer_id": 2,
#         "location_id": 1

#     },
#     {
#         "id": 3,
#         "name": "Blue",
#         "breed": "Cat",
#         "status": "Admitted",
#         "customer_id": 1,
#         "location_id": 2
#     }
# ]


# def get_single_animal(id):
#     # Variable to hold the found animal, if it exists
#     requested_animal = None

#     # Iterate the ANIMALS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for animal in ANIMALS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if animal["id"] == id:
#             requested_animal = animal

#     return requested_animal


# def get_all_animals():
#     return ANIMALS

    #         # Create an animal instance from the current row.
    #         # Note that the database fields are specified in
    #         # exact order of the parameters defined in the
    #         # Animal class above.
    #         animal = Animal(
    #             row['id'],
    #             row['name'],
    #             row['status'],
    #             row['breed'],
    #             row['customer_id'],
    #             row['location_id'])

    #         animals.append(animal.__dict__)

    # # # Use `json` package to properly serialize list as JSON
    # # return json.dumps(animals)


# # Get the id value of the last animal in the list
    # max_id = ANIMALS[-1]["id"]

    # # Add 1 to whatever that number is
    # new_id = max_id + 1

    # # Add an `id` property to the animal dictionary
    # animal["id"] = new_id

    # # Add the animal dictionary to the list
    # ANIMALS.append(animal)

    # # Return the dictionary with `id` property added
    # return animal


# def update_animal(id, new_animal):
#     # Iterate the ANIMALS list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Update the value
#             ANIMALS[index] = new_animal
#             break


# def delete_animal(id):
#     # Initial -1 value for animal index, in case one isn't found
#     animal_index = -1

#     # Iterate the ANIMALS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Store the current index.
#             animal_index = index

#     # If the animal was found, use pop(int) to remove it from list
#     if animal_index >= 0:
#         ANIMALS.pop(animal_index)
