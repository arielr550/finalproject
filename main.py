from stack_queue import Stack, Queue
from linked_list import Node, LinkedList

class Person:
    def __init__(self, p_id: int, name: str, age: int):
        self.person_id = p_id
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person ID: {self.person_id}, Name: {self.name}, Age: {self.age}"

class Customer(Person):
    def __init__(self, p_id: int, name: str, age: int, vip: bool):
        super().__init__(p_id, name, age)
        self.vip = vip

    def __repr__(self):
        return f"{super().__repr__()}, Vip: {self.vip}"

class Employee(Person):
    def __init__(self, p_id: int, name: str, age: int, hour_sal: int):
        super().__init__(p_id, name, age)
        self.hour_sal = hour_sal
        self.work_day = LinkedList()

    def __repr__(self):
        return f"Hour Salary: {self.hour_sal}, Work Day: {self.work_day}"

class WorkDay:
    def __init__(self, day: int, month: int, work_hours: int):
        self.day = day
        self.month = month
        self.work_hours = work_hours

    def __repr__(self):
        return f"Day: {self.day}, Month: {self.month}, Work Hours: {self.work_hours}"

class Suitcase:
    def __init__(self, person: Person, weight: float):
        self.person = person
        self.weight = weight

    def __repr__(self):
        return f"Person: {self.person}, Weight: {self.weight}"

class Flight:
    def __init__(self, f_id: int, destination: str, day: int, month: int, time: int, max_passengers: int, price: int):
        self.flight_id = f_id
        self.dest = destination
        self.day = day
        self.month = month
        self.time = time
        self.max_pass = max_passengers
        self.price = price
        self.people_queue = Queue()
        self.suitcase_stack = Stack()

    def __repr__(self):
        return (f"Flight ID: {self.flight_id}, Destination: {self.dest}, Day: {self.day}, Month: {self.month}, "
                f"Time: {self.time}, Max Passengers: {self.max_pass}, Price: {self.price},"
                f" PeopleQueue: {self.people_queue}, SuitCaseStack: {self.suitcase_stack}")

class Airport:
    def __init__(self, airport_code: str):
        self.airport_code = airport_code
        self.flight_list = []
        self.customer_list = []
        self.employee_list = []

    def add_flight(self):
        print('***Flight Addition***')
        flight_id = int(input('Enter flight id: '))
        dest = input('Enter destination: ')
        day = int(input('Enter day date (number): '))
        month = int(input('Enter month (number): '))
        time = int(input('Enter time (number): '))
        max_p = int(input('Enter max passengers: '))
        price = int(input('Enter price: '))
        flight = Flight(flight_id, dest, day, month, time, max_p, price)
        self.flight_list.append(flight)

    def add_customer(self):
        print('***Customer Addition***')
        p_id = int(input('Enter your ID: '))
        name = input('Enter your name: ')
        age = int(input('Enter your age: '))
        vip = None
        choice = input('Are you a vip? type "yes" or "no": ')
        if choice.lower() == 'yes':
            vip = True
        elif choice.lower() == 'no':
            vip = False
        customer = Customer(p_id, name, age, vip)
        self.customer_list.append(customer)

    def choose_flight(self):
        customer_id = int(input('Enter customer id: '))
        budget = int(input('Enter your budget: '))
        customer = None

        for c in self.customer_list:
            if customer_id == c.person_id:
                customer = c
                break

        if customer is None:
            return f"Customer is not found!"

        possible_flights = [f for f in self.flight_list if f.price <= budget and f.max_pass > f.people_queue.size()]
        if not possible_flights:
            return f"No flight for your budget or not free spaces"







    def __repr__(self):
        return (f"Airport Code: {self.airport_code}, Flight List: {self.flight_list}, Customer List: {self.customer_list},"
                f" Employee List: {self.employee_list}")



person = Person(1, 'Ariel', 26)
airport = Airport('TLV')
# airport.add_flight()
# airport.add_customer()
print(airport)