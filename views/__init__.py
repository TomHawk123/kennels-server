from .animal_requests import get_all_animals, create_animal, delete_animal
from .animal_requests import update_animal, delete_animal, get_animals_by_location_id, get_animals_by_status
from .location_requests import get_all_locations, create_location, delete_location
from .location_requests import update_location
from .customer_requests import get_all_customers, create_customer, delete_customer
from .customer_requests import update_customer, get_customers_by_email
from .customer_requests import get_customers_by_name
from .employee_requests import get_all_employees, create_employee, delete_employee
from .employee_requests import update_employee, get_employees_by_location_id


# __init__.py is being checked on initialization. Provides all exports that
# will be read from a given directory.
