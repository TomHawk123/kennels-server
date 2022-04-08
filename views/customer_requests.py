CUSTOMERS = [
    {
        "id": 1,
        "name": "Zach Dugger"
    },
    {
        "id": 2,
        "name": "Katie Dawkins"
    }
]


def get_all_customers():
    return CUSTOMERS


def get_single_customer(id):
    requested_customer = None

    for customer in CUSTOMERS:
        if customer["id"] == id:
            requested_customer = CUSTOMERS

    return requested_customer
