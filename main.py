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
        # New lists for suitcase choices
        self.no_suitcase_by_choice = []
        self.no_suitcase_overweight = []

    def __repr__(self):
        return (f"Flight ID: {self.flight_id}, Destination: {self.dest}, Day: {self.day}, Month: {self.month}, "
                f"Time: {self.time}, Max Passengers: {self.max_pass}, Price: {self.price}")

class Airport:
    def __init__(self, airport_code: str):
        self.airport_code = airport_code
        self.flight_list = []
        self.customer_list = []
        self.employee_list = []

    def add_flight(self):
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

    def add_customer(self):
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
        customer_id = int(input('Enter Customer ID: '))
        budget = int(input('Enter your budget: '))
        customer = None
        # search for the customer
        for c in self.customer_list:
            if customer_id == c.person_id:
                customer = c
                break
        # check if customer exists
        if customer is None:
            return "Customer is not found!"

        possible_flights = [f for f in self.flight_list if f.price <= budget and f.max_pass > f.people_queue.size()]
        if not possible_flights:
            return "No flight for your budget or not free spaces"
        # choosing a flight
        for flight in possible_flights:
            print(flight)
        choice = int(input('Enter your flight choice: '))
        chosen_flight = None
        for flight in possible_flights:
            if flight.flight_id == choice:
                chosen_flight = flight
                break
        if chosen_flight is None:
            return "Invalid flight choice!"


        suitcase_choice = input('Are you flying with a suitcase? ("yes" or "no"): ')
        if suitcase_choice.lower() == 'yes':
            weight = float(input('What is the weight of the suitcase? '))
            suitcase = Suitcase(customer, weight)

            chosen_flight.people_queue.enqueue(customer)
            chosen_flight.price = chosen_flight.price * 1.02

            if customer.vip:
                #If customer is VIP
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
            
            else:
                # If customer is not VIP
                max_weight = 23 * chosen_flight.max_pass
                current_weight = 0
                temp_stack = Stack()

                while not chosen_flight.suitcase_stack.is_empty():
                    # Pop all the calculate max weight
                    s = chosen_flight.suitcase_stack.pop()
                    current_weight += s.weight
                    temp_stack.push(s)

                while not temp_stack.is_empty():
                    # Stack restore
                    chosen_flight.suitcase_stack.push(temp_stack.pop())

                if current_weight + weight > max_weight:
                    # Check if weight exceeded
                    chosen_flight.no_suitcase_overweight.append(customer)
                    return "Suitcase cannot enter - weight limit exceeded!"
                # Add non-vip suitcase at the top of the stack
                chosen_flight.suitcase_stack.push(suitcase)

        elif suitcase_choice.lower() == 'no':
            chosen_flight.no_suitcase_by_choice.append(customer)
            chosen_flight.people_queue.enqueue(customer)
            chosen_flight.price = chosen_flight.price * 1.02


        return f"{customer.name} was added to flight {chosen_flight.flight_id} to {chosen_flight.dest} successfully!"


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
            if emp.p_id == id_choice:
                employee = emp
                break
        if employee is None:
            return 'No such employee!'
        print('*** Work Day Addition ***')
        day = int(input('Enter day: '))
        month = int(input('Enter month: '))
        work_hours = int(input('Enter amound of work hours: '))
        wd = WorkDay(day, month, work_hours)
        employee.work_day.append(wd)
    
    def employee_salary(self, e_id):
        employee = None
        for emp in self.employee_list:
            if emp.p_id == e_id:
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
        return f"Employee {employee.name}'s salary for {month} is: {monthly_salary}"
    
    def flight_ended(self, flight_id):
        landing_flight = None
        for flight in self.flight_list:
            if flight.flight_id == flight_id:
                landing_flight = flight
                print(f'Flight {flight_id} is landing!')
                break
            else:
                return f'Flight {flight_id} do not exist!'
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
# airport.add_flight()
# airport.add_flight()
# airport.add_customer()
# airport.add_customer()
# print(airport)
# print(airport.choose_flight())
# airport.flight_ended(325)



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
            pass


            
        elif choice == '8':
            e_id = int(input('Enter employee ID: '))
            airport.employee_salary(e_id)


print(menu())