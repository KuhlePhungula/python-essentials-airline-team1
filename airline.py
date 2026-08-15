# Airline Reservation System
# Python Essentials 1 Group Project

# Team Members
# - Kuhlekonke Phungula
# - Uwaiz Lovell


# adds new flight details and builds a seat map
def add_flight(flights, next_flight_number):
    origin = read_nonblank("Origin: ").upper()
    destination = read_nonblank("Destination: ").upper()
    price = read_positive_number("Price: R")
    rows = read_valid_number("Number of rows (1-9): ", 1, 9)
    seats_per_row = read_valid_number("Seats per row (1-6): ", 1, 6)

    seat_map = []
    for row_index in range(rows):
        row = []
        for col_index in range(seats_per_row):
            row.append(" ")
            seat_map.append(row)
        

    flight_id = "F" + str(next_flight_number)
    flights[flight_id] = {
        "origin": origin,
        "dest": destination,
        "price": price,
        "seats": seat_map,
        "waitlist": []
    }

    print("Added", flight_id, ":", origin, "->", destination, "|", "R", format(price, ".2f"), "|", str(rows, "rows x", str(seats_per_row), "seats"))
    return next_flight_number + 1


# converts seat labels to indexes and return (row_index, col_index)
def seat_label_to_indexes(seat_label):
    if seat_label is None:
        return None, None

    seat_label = seat_label.strip().upper()
    if seat_label == "":
        return None, None

    row_block = ""
    col_block = ""
    for block in seat_label:
        if block.isdigit():
            if col_block != "":
                return None, None
            row_block += block
        elif block.isalpha():
            col_block += block
        else: 
            return None, None

    if row_block == "" or len(col_block) != 1:
        return None, None
    if col_block not in seat_letters:
        return None, None

    row_index = int(row_block) - 1
    col_index = seat_letters.index(col_block)
    if row_block < 0:
        return None, None

    return row_index, col_index


def render_seat_map(flights):
    flight_id = read_nonblank("Flight ID: ").upper()
    if flight_id not in flights:
        print("Flight", flight_id, "not found.")
        return False

    flight = flights[flight_id]
    seats = flights["seats"]
    rows = len(seats)
    seats_per_row = len(seats[0]) if rows > 0 else 0

    print("\nFlight", flight_id, ":", flight["origin"], "->", flight["dest"], "|", "R", format(flight["price"], ".2f"), "|", str(rows, "rows x", str(seats_per_row), "seats"))

    header = "   "
    for col_index in range(seats_per_row):
        header += "  " + seat_letters[col_index] + "  "
        print(header)

    for row_index in range(rows):
        line = str(row_index + 1) + "  "
        for col_index in range(seats_per_row):
            line += "[" + seats[row_index][col_index] + "]"
        print(line)

    taken, total = seat_counts(seats)
    percent = (taken / total * 100) if total > 0 else 0.0
    print("Seats taken: ", str(taken), "of", str(total) + "(", format(percent, ".1f"), "% full)")
    return True


# counts how many seats are taken compared to total seats on a flight's seat map
def seat_counts(seats):
    total = 0
    taken = 0

    for row in seats:
        for block in row:
            total += 1
            if block == "X":
                taken += 1
    return taken, total


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
seat_letters = "ABCDEF"

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
    


