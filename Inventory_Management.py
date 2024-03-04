import sqlite3
import time
import sys
import random
from datetime import datetime
from math import radians, cos, sin, asin, sqrt


def printf(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    print()


def haversine(point1, point2, units="mi"):
    """ Calculate an approximate distance between two points on Earth.

    Args:
        point1 (tuple of float, float): first point (lat, lon) in
            decimal degrees.
        point2 (tuple of float, float): second point (lat, lon) in
            decimal degrees.
        units (str): units of return value. Should be "km" for
            kilometers or "mi" for miles. (Default: "km")

    Returns:
        float: the distance between the two points in the requested
        units.
    """
    if units not in ["km", "mi"]:
        raise ValueError("units should be 'km' or 'mi'")
    R = 6372.8 if units == "km" else 3959.87433

    if len(point1) != 2:
        raise ValueError("point1 should be a tuple of two floats")
    if len(point2) != 2:
        raise ValueError("point2 should be a tuple of two floats")
    lat1, lon1 = point1
    lat2, lon2 = point2
    for value in [lat1, lon1, lat2, lon2]:
        if not isinstance(value, (float, int)):
            raise ValueError("coordinates must be floats")

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c


class BaseEntity:
    def __init__(self, db_file):
        self.db_file = db_file

    def drop_table(self, table_name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        conn.commit()
        conn.close()


class Inventory(BaseEntity):
    def __init__(self, db_file='inventory.db'):
        super().__init__(db_file)
        self.drop_table('inventory')
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    item_description TEXT,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    machine_type TEXT NOT NULL
                )
            ''')

        conn.commit()
        conn.close()

    def populate_inventory(self, file_path):
        with open(file_path, 'r') as file:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            for line in file:
                values = list(map(str.strip, line.split(',')))
                item_name, item_description, price, quantity, machine_type = values[0:5]
                cursor.execute(
                    'INSERT INTO inventory (item_name, item_description, price, quantity, machine_type) '
                    'VALUES (?, ?, ?, ?, ?)',
                    (item_name, item_description, float(price), int(quantity), machine_type))

            conn.commit()
            conn.close()

    def display_inventory(self, items_to_display=None):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        print("Here are all the items in the inventory: ")
        if items_to_display:
            for item in items_to_display:
                print(
                    f"ID: {item[0]}, Name: {item[1]}, Description: {item[2]}, Price: {item[3]}, Quantity: {item[4]},"
                    f" Type: {item[5]}")
        else:
            cursor.execute('SELECT * FROM inventory')
            items = cursor.fetchall()

            if not items:
                print("Inventory is empty.")
            else:
                for item in items:
                    print(
                        f"ID: {item[0]}, Name: {item[1]}, Description: {item[2]}, Price: {item[3]}, Quantity: {item[4]}"
                        f", Type: {item[5]}")

        conn.close()

    def get_items_by_type(self, machine_type):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM inventory WHERE machine_type = ?', (machine_type,))
        items = cursor.fetchall()

        conn.close()

        return items

    def check_quantity_available(self, item_id, quantity_needed):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT quantity FROM inventory WHERE id = ?', (item_id,))
        available_quantity = cursor.fetchone()[0]

        conn.close()

        return available_quantity >= quantity_needed

    def deduct_inventory_quantity(self, item_id, quantity_needed):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            cursor.execute('UPDATE inventory SET quantity = quantity - ? WHERE id = ?', (quantity_needed, item_id))
            conn.commit()
            print(f"{quantity_needed} units deducted from inventory for item ID {item_id}")
        except sqlite3.Error as e:
            print(f"Error deducting inventory quantity: {e}")
        finally:
            conn.close()


class Customer(BaseEntity):
    def __init__(self, db_file='inventory.db'):
        super().__init__(db_file)
        self.drop_table('customers')
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone_number TEXT, 
                operating_hours TEXT,
                latitude REAL, 
                longitude REAL
            )
        ''')

        conn.commit()
        conn.close()

    def populate_customers(self, file_path):
        with open(file_path, 'r') as file:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            for line in file:
                values = list(map(str.strip, line.split(',')))

                name = values[0]
                address = ', '.join(values[1:4])
                phone_number = values[-4]
                operating_hours = values[-3]
                latitude = float(values[-2])
                longitude = float(values[-1])

                cursor.execute(
                    'INSERT INTO customers (name, address, phone_number, operating_hours, latitude, longitude) '
                    'VALUES (?, ?, ?, ?, ?, ?)',
                    (name, address, phone_number, operating_hours, latitude, longitude))

            conn.commit()
            conn.close()

    def display_customers(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()

        for customer in customers:
            print(
                f"ID: {customer[0]}, Name: {customer[1]}, Address: {customer[2]}, Phone Number: {customer[3]}, "
                f"Operating Hours: {customer[4]}, Latitude: {customer[5]}, Longitude: {customer[6]}")

        # Close the connection
        conn.close()

    def get_coordinates_by_id(self, customer_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT latitude, longitude FROM customers WHERE id = ?', (customer_id,))
        coordinates = cursor.fetchone()

        conn.close()

        return coordinates


class Machines(BaseEntity):
    def __init__(self, db_file='inventory.db'):
        super().__init__(db_file)
        self.drop_table('machines')
        self.create_table()
        self.service_history = []
        self.distinct_machines = set()

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS machines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                manufacturer TEXT NOT NULL,
                name TEXT NOT NULL,
                machine_type TEXT NOT NULL,
                serial_number TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        conn.commit()
        conn.close()

    def populate_machines(self, file_path):
        with open(file_path, 'r') as file:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            for line in file:
                values = list(map(str.strip, line.split(',')))

                machine_data = {
                    'manufacturer': values[0],
                    'name': values[1],
                    'machine_type': values[2],
                    'serial_number': values[3],
                    'status': values[4],
                    'customer_id': values[5]
                }

                cursor.execute(
                    'INSERT INTO machines (customer_id, manufacturer, name, machine_type, serial_number, status)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (machine_data['customer_id'], machine_data['manufacturer'], machine_data['name'],
                     machine_data['machine_type'], machine_data['serial_number'], machine_data['status']))

            conn.commit()
            conn.close()

    def generate_machine_issues(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM machines')
        machines = cursor.fetchall()

        machines_to_update = random.sample(machines, random.randint(1, 8))

        for machine in machines_to_update:
            machine_id = machine[0]
            cursor.execute('UPDATE machines SET status = "Need Repair" WHERE id = ?', (machine_id,))

        conn.commit()
        conn.close()

    def display_machines(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT machines.id, customers.name, machines.manufacturer, machines.name, machines.machine_type, 
            machines.serial_number, machines.status
            FROM machines
            INNER JOIN customers ON machines.customer_id = customers.id
        ''')

        machines = cursor.fetchall()

        for machine in machines:
            print(
                f"{machine[2]} {machine[3]}, Serial Number: {machine[5]},Customer: {machine[1]}, Status: {machine[6]}")

        conn.close()

    def display_distinct_machines(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT manufacturer, name
            FROM machines
        ''')

        machines_set = set(cursor.fetchall())

        sorted_machines = sorted(machines_set, key=lambda machine: (machine[0], machine[1]))

        for machine in sorted_machines:
            print(f"{machine[0]} {machine[1]}")

        conn.close()

    def display_machines_repair(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM machines WHERE status = "Need Repair"')
        machines = cursor.fetchall()

        for machine in machines:
            print(
                f"ID: {machine[0]}, Customer ID: {machine[1]}, Machine Name: {machine[2]}, Type: {machine[4]}, "
                f"Serial Number: {machine[5]}, Status: {machine[6]}")

        conn.close()

    def repair_machine(self, machine_id, inventory):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM machines WHERE id = ?', (machine_id,))
            machine = cursor.fetchone()

            if machine:
                inventory_type = machine[4]
                items_for_repair = inventory.get_items_by_type(inventory_type)

                print(f"Choose items from the inventory for the repair ({inventory_type}):")
                inventory.display_inventory(items_for_repair)

                # Ask the user to choose an item and quantity
                item_id = int(input("Enter the ID of the item you need for the repair: "))
                quantity_needed = int(input("Enter the quantity needed: "))

                if inventory.check_quantity_available(item_id, quantity_needed):
                    inventory.deduct_inventory_quantity(item_id, quantity_needed)

                    cursor.execute('UPDATE machines SET status = "Good" WHERE id = ?', (machine_id,))
                    conn.commit()

                    service_info = {
                        'machine_id': machine_id,
                        'item_id': item_id,
                        'quantity_used': quantity_needed,
                        'repair_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self.service_history.append(service_info)

                    print(f"Machine with ID {machine_id} has been repaired and set to 'Good' status.")
                    print(f"Inventory updated. {quantity_needed} units of item ID {item_id} deducted.")
                else:
                    print("Insufficient quantity in the inventory. Repair cannot be completed.")

            else:
                print(f"No machine found with ID {machine_id}.")

        except sqlite3.Error as e:
            print(f"Error repairing machine: {e}")

        finally:
            conn.close()

    def display_service_history(self):
        if len(self.service_history) == 0:
            print("There hasn't been any service repairs")
            time.sleep(2)
        else:
            print("Service History:")
        for entry in self.service_history:
            print(f"Machine ID: {entry['machine_id']}, Item ID: {entry['item_id']}, "
                  f"Quantity Used: {entry['quantity_used']}, Repair Date: {entry['repair_date']}")


if __name__ == "__main__":

    inventory = Inventory()
    customer = Customer()
    machines = Machines()

    inventory_path = 'inventoryList.txt'
    inventory.populate_inventory(inventory_path)

    customer_path = 'customerList.txt'
    customer.populate_customers(customer_path)

    machines_path = 'machinesList.txt'
    machines.populate_machines(machines_path)
    machines.generate_machine_issues()

    printf("Welcome To the Service Technician Management System!")
    while True:
        try:
            print("\nPick an option below: ")
            print(
                "1. View Machines in Need of Repair\n2. Calculate Distance Between Two Customer Locations\n"
                "3. View Inventory\n4. View Customers\n"
                "5. View All machines and Their Locations\n6. View Service History\n7. View All Machines That Are Able"
                " ""To Be Ordered\nType 'quit' to exit")
            choice = input('Choice 1-7: ')
            print()

            if choice.lower() == 'quit':
                print("Thank you for using the Service Technician Management System. Goodbye!")
                break

            choice = int(choice)

            if choice == 1:
                print("Here is a list of all machines in need of repair: ")
                machines.display_machines_repair()
                # Ask the user for the machine ID to repair
                machine_id = int(input("Enter the ID of the machine to repair: "))
                machines.repair_machine(machine_id, inventory)
            elif choice == 2:
                print("Here is a list of all machines at all locations: ")
                customer.display_customers()
                customer1_id = int(input("Choose the first customer ID you'd like to start from: "))
                customer2_id = int(input("Choose the second customer ID you'd like to stop at: "))
                customer1_coordinates = customer.get_coordinates_by_id(customer1_id)
                customer2_coordinates = customer.get_coordinates_by_id(customer2_id)
                distance = haversine(customer1_coordinates, customer2_coordinates)

                print(f"The distance between the two customers is {distance:.2f} miles.")
            elif choice == 3:
                inventory.display_inventory()
            elif choice == 4:
                customer.display_customers()
            elif choice == 5:
                machines.display_machines()
            elif choice == 6:
                machines.display_service_history()
            elif choice == 7:
                machines.display_distinct_machines()

        except ValueError:
            print("Invalid input. Please enter a valid number or 'quit' to exit.")
