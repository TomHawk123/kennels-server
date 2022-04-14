from models.animal import Animal
from models.customer import Customer
from models.employee import Employee
import json
import sqlite3
from models.location import Location


def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.id location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN Location l
            ON l.id = e.location_id
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            employee = Employee(row['id'],
                                row['name'],
                                row['address'],
                                row['location_id']
                                )

            location = Location(row['id'],
                                row['location_name'],
                                row['location_address'],
                                )

            employee.location = location.__dict__

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)


def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.id location_id,
            l.name location_name,
            l.address location_address,
            a.id animal_id,
            a.name animal_name,
            a.status animal_status,
            a.breed animal_breed,
            a.customer_id animal_customer_id,
            a.location_id animal_location_id
        FROM employee e
        JOIN location l
            ON l.id = e.location_id
        JOIN animal a
            ON a.location_id = e.location_id
        WHERE e.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        location = Location(data['location_id'],
                            data['location_name'],
                            data['location_address'])

        animal = Animal(data['animal_id'],
                        data['animal_name'],
                        data['animal_status'],
                        data['animal_breed'],
                        data['animal_customer_id'],
                        data['animal_location_id']
                        )

        # Create an employee instance from the current row
        employee = Employee(data['id'],
                            data['name'],
                            data['address'],
                            data['location_id'],
                            location.__dict__,
                            animal.__dict__
                            )

        return json.dumps(employee.__dict__)


def get_employees_by_location_id(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.address,
            e.location_id
            FROM employee e
            WHERE e.location_id = ?
            """, (location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row['id'],
                row['name'],
                row['address'],
                row['location_id']
            )
            employees.append(employee.__dict__)

    return json.dumps(employees)


def create_employee(new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
        (name,
        address,
        location_id
        )
        VALUES ( ?, ?, ? );
        """, (
            new_employee['name'],
            new_employee['address'],
            new_employee['location_id']
        ))

        id = db_cursor.lastrowid

        new_employee['id'] = id

    return json.dumps(new_employee)


def delete_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))


def update_employee(id, new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Employee
            SET
                name = ?,
                address = ?,
                email = ?,
                password = ?,
        WHERE id = ?
        """, (
            new_employee['name'],
            new_employee['address'],
            new_employee['locationId'],
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


# ORIGINAL CODE
# EMPLOYEES = [
#     {
#         "id": 1,
#         "name": "Christian Haggerty"
#     },
#     {
#         "id": 2,
#         "name": "Ari Daron"
#     }
# ]


# def get_all_employees():
#     return EMPLOYEES


# def get_single_employee(id):
#     requested_employee = None

#     for employee in EMPLOYEES:
#         if employee["id"] == id:
#             requested_employee = employee

#     return requested_employee


# def delete_employee(id):
#     # Initial -1 value for employee index, in case one isn't found
#     employee_index = -1

#     # Iterate the EMPLOYEES list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the employee. Store the current index.
#             employee_index = index

#     # If the employee was found, use pop(int) to remove it from list
#     if employee_index >= 0:
#         EMPLOYEES.pop(employee_index)


# def update_employee(id, new_employee):

#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             EMPLOYEES[index] = new_employee
#             break


# def create_employee(employee):
#     max_id = EMPLOYEES[-1]["id"]

#     new_id = max_id + 1

#     employee["id"] = new_id

#     EMPLOYEES.append(employee)

#     return employee
