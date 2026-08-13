# Airline Reservation System
# Python Essentials 1 Group Project

# Team Members
# - Kuhlekonke Phungula
# - Uwaiz Lovell



def add_flight():
    pass


def seat_label_to_indexes():
    pass


def render_seat_map():
    pass


def seat_counts():
    pass


# Registers new passenger with automatic ID and adds them to the passengers dictionary
def register_passenger(passengers, next_passenger_number):
    name = read_nonblank("Enter passenger name: ")
    passenger_id = "P" + str(next_passenger_number)
    passengers[passenger_id] = {"name": name}
    next_passenger_number += 1
    print("Registered", passenger_id, ":", name)
    return passengers
    

def book_seat():
    pass


def cancel_booking():
    pass


def change_seat():
    pass


def join_waitlist():
    pass


def promote_from_waitlist():
    pass


def flight_manifest():
    pass


def revenue_report():
    pass


def find_passenger_booking():
    pass


def calculate_flight_revenue():
    pass


# Validates whole number input within low and high, and reprompts on bad input
def read_valid_number(prompt, low, high):
    while True:
        try:
            number = int(input(prompt))
            if low <= number <= high:
                return number
            else:
                print("Please enter a number between" + str(low) + "and" + str(high) + ".")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Checks for blank input an reprompts until something is typed in 
def read_nonblank(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            print("Input cannot be blank. Please try again.")
        else:
            return text


# Checks for positive number input, used for prices entry, and reprompts on bad input
def read_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid input.")


# main program
flights = {}
passengers = {}
bookings = {}
next_passenger_number = 1
next_flight_number = 1 
next_booking_number = 1

while True:
    print("\n===== SKYLINK RESERVATIONS =====")
    print("1. Add flight")
    print("2. Register a passenger")
    print("3. View seat map")
    print("4. Book a seat")
    print("5. Cancel a booking")
    print("6. Change a seat")
    print("7. Flight Manifest")
    print("8. Revenue report")
    print("9. Exit")

    choice = read_valid_number("Welcome to SKYLINK. Choose an option (1-9): ", 1, 9)

    if choice == 1:
        add_flight()
    elif choice == 2:
        register_passenger()
    elif choice == 3:
        render_seat_map()
    elif choice == 4:
        book_seat()
    elif choice == 5:
        cancel_booking()
    elif choice == 6:
        change_seat()
    elif choice == 7:
        flight_manifest()
    elif choice == 8:
        revenue_report()
    elif choice == 9:
        print("Exiting SKYLINK. Goodbye.")
        break
    


