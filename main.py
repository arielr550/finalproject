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
        self.people_queue = Queue() # Queue of customers (FIFO)
        self.suitcase_stack = Stack() # Stack of suitcases (LIFO)
        self.no_suitcase_by_choice = [] # Customers who chose to fly without suitcase
        self.no_suitcase_overweight = [] # Customers denied suitcase due to overweight

    def __repr__(self):
        return (f"Flight ID: {self.flight_id}, Destination: {self.dest}, Day: {self.day}, Month: {self.month}, "
                f"Time: {self.time}, Max Passengers: {self.max_pass}, Price: {self.price}")

class Airport:
    def __init__(self, airport_code: str):
        self.airport_code = airport_code
        self.flight_list = []
        self.customer_list = []
        self.employee_list = []

    # -------- FLIGHT MANAGEMENT --------

    def add_flight(self):
        """Creates and adds a new flight to the airport's flight list. """
        print('*** Flight Addition ***')
        flight_id = int(input('Enter Flight ID: '))
        dest = input('Enter Destination: ')
        day = int(input('Enter day date (number): '))
        month = int(input('Enter month (number): '))
        time = int(input('Enter time (number): '))
        max_p = int(input('Enter max passengers: '))
        price = int(input('Enter price: '))
        flight = Flight(flight_id, dest, day, month, time, max_p, price)
        self.flight_list.append(flight)


        # -------- CUSTOMER MANAGEMENT --------

    def add_customer(self):
        """Registers a new customer (VIP or regular)."""
        print('*** Customer Addition ***')
        p_id = int(input('Enter your ID: '))
        name = input('Enter your name: ')
        age = int(input('Enter your age: '))
        vip = True
        choice = input('Are you a vip? type "yes" or "no": ')
        if choice.lower() == 'yes':
            vip = True
        elif choice.lower() == 'no':
            vip = False
        customer = Customer(p_id, name, age, vip)
        self.customer_list.append(customer)

    def choose_flight(self):
        """
        Allows a customer to choose a flight based on their budget and flight availability.
        Handles adding them to the flight queue and processing suitcase logic:
            - VIP customers' suitcases are placed above all regulars (LIFO priority).
            - Non-VIPs must respect a total weight limit (23 kg * max passengers).
            - Each added customer increases the flight's ticket price by 2%.
        """
        customer_id = int(input('Enter Customer ID: '))
        budget = int(input('Enter your budget: '))
        customer = None

        # search for the customer by ID
        for c in self.customer_list:
            if customer_id == c.person_id:
                customer = c
                break
        
        # check if customer exists
        if customer is None:
            return "Customer is not found!"

        # Find flights matching budget and seat availability
        possible_flights = [f for f in self.flight_list if f.price <= budget and f.max_pass > f.people_queue.size()]
        if not possible_flights:
            return "No flight for your budget or not free spaces"
        
        # Display available flights
        print('\nAvailable flights:')
        for flight in possible_flights:
            print(flight)
        
        # customer chooses flight by ID
        choice = int(input('Enter your flight choice: '))
        chosen_flight = None
        for flight in possible_flights:
            if flight.flight_id == choice:
                chosen_flight = flight
                break
        if chosen_flight is None:
            return "Invalid flight choice!"
        
        # Add customer to flight queue and increase price by 2%
        chosen_flight.people_queue.enqueue(customer)
        chosen_flight.price = chosen_flight.price * 1.02

        # suitcase logic
        suitcase_choice = input('Are you flying with a suitcase? ("yes" or "no"): ')
        if suitcase_choice.lower() == 'yes':
            weight = float(input('What is the weight of the suitcase? '))
            suitcase = Suitcase(customer, weight)

            # VIP suitcase handling (priority placement)
            if customer.vip:
                if chosen_flight.suitcase_stack.is_empty():
                    # If stack is empty, just pushing the suitcase
                    chosen_flight.suitcase_stack.push(suitcase)
                else:
                    # Creating a temp stack to reorder
                    temp_stack = Stack()
                    while not chosen_flight.suitcase_stack.is_empty():
                        top_suitcase = chosen_flight.suitcase_stack.peek()
                        if top_suitcase.person.vip:
                            break
                        temp_stack.push(chosen_flight.suitcase_stack.pop())
                    chosen_flight.suitcase_stack.push(suitcase)
                    while not temp_stack.is_empty():
                        chosen_flight.suitcase_stack.push(temp_stack.pop())


            # Regular (non-VIP) suitcase handling with weight limit
            else:
                max_weight = 23 * chosen_flight.max_pass
                current_weight = 0
                temp_stack = Stack()

                while not chosen_flight.suitcase_stack.is_empty():
                    # Pop all the calculate max weight
                    s = chosen_flight.suitcase_stack.pop()
                    current_weight += s.weight
                    temp_stack.push(s)


                if current_weight + weight > max_weight:
                    # Restore stack and record overweight case
                    while not temp_stack.is_empty():
                        chosen_flight.suitcase_stack.push(temp_stack.pop())
                    chosen_flight.no_suitcase_overweight.append(customer)
                    return "Suitcase cannot enter - weight limit exceeded!"
                
                # Add non-vip suitcase at the top of the stack
                chosen_flight.suitcase_stack.push(suitcase)
                while not temp_stack.is_empty():
                    chosen_flight.suitcase_stack.push(temp_stack.pop())

        elif suitcase_choice.lower() == 'no':
            chosen_flight.no_suitcase_by_choice.append(customer)

        return f"{customer.name} was added to flight {chosen_flight.flight_id} to {chosen_flight.dest} successfully!"

        # -------- EMPLOYEE MANAGEMENT --------

    def add_employee(self):
        # p_id: int, name: str, age: int, hour_sal: int
        e_id = int(input('Enter your ID: '))
        name = input('Enter your name: ')
        age = int(input('Enter your age: '))
        hour_sal = int(input('Enter your hourly salary: '))
        emp = Employee(e_id, name, age, hour_sal)
        self.employee_list.append(emp)
    
    def add_workday(self):
        employee = None
        id_choice = int(input('Enter Employee ID: '))
        for emp in self.employee_list:
            if emp.person_id == id_choice:
                employee = emp
                break
        if employee is None:
            return 'No such employee!'
        print('*** Work Day Addition ***')
        day = int(input('Enter day: '))
        month = int(input('Enter month: '))
        work_hours = int(input('Enter amount of work hours: '))
        wd = WorkDay(day, month, work_hours)
        employee.work_day.append(wd)
    
    def employee_salary(self, e_id):
        employee = None
        for emp in self.employee_list:
            if emp.person_id == e_id:
                employee = emp
        if employee is None:
            return 'No such employee!'
        month = int(input('Enter month: '))
        total_hours = 0
        current = employee.work_day.head
        while current:
            if current.value.month == month:
                total_hours += current.value.work_hours
            current = current.next
        monthly_salary = total_hours * employee.hour_sal
        return monthly_salary
    
    # פונקציית עזר עם חודש כפרמטר
    def get_employee_salary(self, e_id, month):
        employee = None
        for emp in self.employee_list:
            if emp.person_id == e_id:
                employee = emp
                break
        if employee is None:
            return 'No such employee!'
        total_hours = 0
        current = employee.work_day.head
        while current:
            if current.value.month == month:
                total_hours += current.value.work_hours
            current = current.next
        monthly_salary = total_hours * employee.hour_sal
        return monthly_salary

    
    def flight_ended(self, flight_id):
        """Simulates flight landing — unloads suitcases and shows who didnt bring one."""
        landing_flight = None
        for flight in self.flight_list:
            if flight.flight_id == flight_id:
                landing_flight = flight
                print(f'Flight {flight_id} is landing!')
                break
        if landing_flight is None:
            return f'Flight {flight_id} do not exist'
        
        print('*** Suitcases Incoming ***')
        while not landing_flight.suitcase_stack.is_empty():
            print(landing_flight.suitcase_stack.pop())
        if landing_flight.no_suitcase_by_choice:
            print('Names of people without suitcase by choice: ')
            for customer in landing_flight.no_suitcase_by_choice:
                print(customer.name)
        if landing_flight.no_suitcase_overweight:
            print('Names of people without suitcase because overweight: ')
            for customer in landing_flight.no_suitcase_overweight:
                print(customer.name)        


    def __repr__(self):
        return (f"Airport Code: {self.airport_code}, Flight List: {self.flight_list}, Customer List: {self.customer_list},"
                f" Employee List: {self.employee_list}")



airport = Airport('TLV')


def quick_sort(lst):
    """Sorts a list of (name, salary) tuples in descending order of salary."""
    if len(lst) <= 1:
        return lst
    pivot = lst[0]
    smaller = [x for x in lst[1:] if x[1] < pivot[1]]
    greater = [x for x in lst[1:] if x[1] >= pivot[1]]
    return quick_sort(greater) + [pivot] + quick_sort(smaller)

def menu():
    print(f"Welcome to {airport.airport_code} Airport, please select an option: ")
    print('===============================')
    print('1. Add a flight')
    print('2. Register new customer')
    print('3. Get flight recommendation')
    print('4. View landing flight summary')
    print('5. Register new employee')
    print('6. Update employee work hours')
    print('7. View sorted employee salaries')
    print('8. Display employee salary by ID')
    print('Type "quit" to exit')
    print('===============================')

    while True:
        choice = input('\nEnter your choice (1-8 or "quit"): ')
        if choice.lower() == 'quit':
            print('Goodbye!')
            break
        elif choice == '1':
            airport.add_flight()
        elif choice == '2':
            airport.add_customer()
        elif choice == '3':
            airport.choose_flight()
        elif choice == '4':
            f_id = int(input('Enter flight ID: '))
            airport.flight_ended(f_id)
        elif choice == '5':
            airport.add_employee()
        elif choice == '6':
            airport.add_workday()
        elif choice == '7':
            # sort salaries
            emp_salaries = []
            month = int(input('Enter month for salary info: '))
            for emp in airport.employee_list:
                salary = airport.get_employee_salary(emp.person_id, month)
                if isinstance(salary, int):
                    emp_salaries.append((emp.name, salary))
            sorted_salaries = quick_sort(emp_salaries)
            print('\nEmployee Salaries (Sorted):')
            print(sorted_salaries)
                
        elif choice == '8':
            e_id = int(input('Enter employee ID: '))
            result = airport.employee_salary(e_id)
            print(f'Monthly salary is: {result}')


menu()
