from models.location import Location
import sqlite3
import json


def create_location(new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Location
        (name,
        address
        )
        VALUES( ?, ?);
        """, (
            new_location['name'],
            new_location['address']
        ))

        id = db_cursor.lastrowid

        new_location['id'] = id

    return json.dumps(new_location)


def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """)

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            location = Location(row['id'],
                                row['name'],
                                row['address']
                                )

            locations.append(location.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(locations)


def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an location instance from the current row
        location = Location(data['id'],
                            data['name'],
                            data['address']
                            )

        return json.dumps(location.__dict__)


def update_location(id, new_location):
    with sqlite3.connect("./kennel-sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Location
            SET
                name = ?,
                address = ?
        WHERE id = ?
        """, (
            new_location['name'],
            new_location['address'],
            id, ))  # <--tuple to look for, kinda like useEffect array.

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))


# ORIGINAL CODE
# LOCATIONS = [
#     {
#         "id": 1,
#         "name": "Nashville North",
#         "address": "8422 Johnson Pike"
#     },
#     {
#         "id": 2,
#         "name": "Nashville South",
#         "address": "209 Emory Drive"
#     }
# ]


# def get_all_locations():
#     return LOCATIONS


# def get_single_location(id):
#     requested_location = None

#     for location in LOCATIONS:
#         if location["id"] == id:
#             requested_location = location

#     return requested_location


# def create_location(location):
#     # Get the id value of the last location in the list
#     max_id = LOCATIONS[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an 'id' property to the location dictionary
#     location["id"] = new_id

#     # Add the location dictionary to the list
#     LOCATIONS.append(location)

#     # Return the dictionary with 'id' property added
#     return location


# def delete_location(id):
#     # Initial -1 value for location index, in case one isn't found
#     location_index = -1

#     # Iterate the LOCATIONS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, location in enumerate(LOCATIONS):
#         if location["id"] == id:
#             # Found the location. Store the current index.
#             location_index = index

#     # If the location was found, use pop(int) to remove it from list
#     if location_index >= 0:
#         LOCATIONS.pop(location_index)


# def update_location(id, new_location):

#     for index, location in enumerate(LOCATIONS):
#         if location["id"] == id:
#             LOCATIONS[index] = new_location
#             break
