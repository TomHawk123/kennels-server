from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views.animal_requests import get_animals_by_status, get_single_animal, get_all_animals, get_animals_by_location_id
from views.animal_requests import delete_animal, update_animal, create_animal
from views.customer_requests import get_all_customers, get_customers_by_email, get_customers_by_name
from views.customer_requests import get_single_customer, create_customer
from views.customer_requests import delete_customer, update_customer
from views.employee_requests import get_all_employees, get_employees_by_location_id, get_single_employee, create_employee, delete_employee, update_employee
from views.location_requests import get_all_locations, get_single_location, create_location, delete_location, update_location


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        response = {}  # Default response
        # Set the response code to 'Ok'
        self._set_headers(200)

        # Parse the URL and capture the tuple that is returned
        # OG code -->(resource, id) = self.parse_url(self.path)

        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # '/animals' or '/animals/2'
        if len(parsed) == 2:
            (resource, id) = parsed

        # Your new console.log() that outputs to the terminal
        # print(self.path)

        # It's an if..else statement
        # if self.path == "/animals":
            if resource == "animals":
                if id is not None:
                    # In Python, this is a list of dictionaries
                    # In JavaScript, you would call it an array of objects
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
                    print(response)
            if resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"
                    # In Python, this is a list of dictionaries
                    # In JavaScript, you would call it an array of objects

            if resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"

            if resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # '/resource?parameter=value'
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            # Is the resource 'customers' and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)

            if key == "name" and resource == "customers":
                response = get_customers_by_name(value)

            if key == "location_id" and resource == "animals":
                response = get_animals_by_location_id(value)

            if key == "location_id" and resource == "employees":
                response = get_employees_by_location_id(value)

            if key == "status" and resource == "animals":
                response = get_animals_by_status(value)

        # This weird code sends a response back to the client
        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server
        """
        # Set response code to 'Created'
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_location = None
        new_employee = None
        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)
            self.wfile.write(f"{new_animal}".encode())

        if resource == "locations":
            new_location = create_location(post_body)
            self.wfile.write(f"{new_location}".encode())

        if resource == "employees":
            new_employee = create_employee(post_body)
            self.wfile.write(f"{new_employee}".encode())

        if resource == "customers":
            new_customer = create_customer(post_body)
            self.wfile.write(f"{new_customer}".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if resource == "customers":
            success = update_customer(id, post_body)

        if resource == "employees":
            success = update_employee(id, post_body)

        if resource == "locations":
            success = update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
            self.wfile.write("".encode())

        if resource == "locations":
            delete_location(id)
            self.wfile.write("".encode())

        if resource == "customers":
            delete_customer(id)
            self.wfile.write("".encode())

        if resource == "employees":
            delete_employee(id)

        # Encode the new animal and send in response
            self.wfile.write("".encode())


def main():
    # This function is not inside the class. It is the starting
    # point of this application
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


# __name__ is referring to THIS project file. Happens on startup
if __name__ == "__main__":
    main()


# ORIGINAL CODE
# def parse_url(self, path):
#     # Just like splitting a string in JavaScript. If the
#     # path is "/animals/1", the resulting list will
#     # have "" at index 0, "animals" at index 1, and "1"
#     # at index 2.
#     path_params = path.split("/")
#     resource = path_params[1]
#     id = None

#     # Try to get the item at index 2
#     try:
#         # Convert the string "1" to the integer 1
#         # This is the new parseInt()
#         id = int(path_params[2])
#     except IndexError:
#         pass  # No route parameter exists: /animals
#     except ValueError:
#         pass  # Request had trailing slash: /animals/

#     return (resource, id)  # This is a tuple

# Encode the new animal and send in response

# # Here's a method on the class that overrides the parent's method.
# # It handles any PUT request.
# def do_PUT(self):
#     """Handles PUT requests to the server
#     """
#     self._set_headers(204)
#     content_len = int(self.headers.get('content-length', 0))
#     post_body = self.rfile.read(content_len)
#     post_body = json.loads(post_body)

#     # Parse the URL
#     (resource, id) = self.parse_url(self.path)

#     # Delete a single animal from the list
#     if resource == "animals":
#         update_animal(id, post_body)

#     if resource == "locations":
#         update_location(id, post_body)

#     if resource == "customers":
#         update_customer(id, post_body)

#     if resource == "employees":
#         update_employee(id, post_body)
#     # Encode the new animal and send in response
#     self.wfile.write("".encode())
#     # self.do_POST()
