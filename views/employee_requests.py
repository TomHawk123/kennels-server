EMPLOYEES = [
    {
        "id": 1,
        "name": "Christian Haggerty"
    },
    {
        "id": 2,
        "name": "Ari Daron"
    }
]


def get_all_employees():
    return EMPLOYEES


def get_single_employee(id):
    requested_employee = None

    for employee in EMPLOYEES:
        if employee["id"] == id:
            requested_employee = EMPLOYEES

    return requested_employee
