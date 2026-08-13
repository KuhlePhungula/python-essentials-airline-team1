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
    

# Books a passenger into an available seat on a flight
def book_seat(flights, passengers, bookings, next_booking_number):

    # Ask for the passenger ID
    passenger_id = input("Passenger ID: ").strip().upper()

    # Check that the passenger exists
    if passenger_id not in passengers:
        print("Passenger does not exist.")
        return bookings, next_booking_number

    # Ask for the flight ID
    flight_id = input("Flight ID: ").strip().upper()

    # Check that the flight exists
    if flight_id not in flights:
        print("Flight does not exist.")
        return bookings, next_booking_number

    # Get the selected flight
    flight = flights[flight_id]

    # Count the seats on the flight
    taken, total = seat_counts(flight["seats"])

    # Check if the flight is full
    if taken == total:
        print("Flight", flight_id, "is FULL.")

        # Ask if the passenger wants to join the waitlist
        answer = input(
            "Add " + passenger_id + " to the waitlist? (y/n): "
        ).strip().lower()

        if answer == "y":

            # Check that the passenger is not already waiting
            if passenger_id in flight["waitlist"]:
                print(passenger_id, "is already on the waitlist.")
            else:
                flight["waitlist"].append(passenger_id)
                position = len(flight["waitlist"])

                print(
                    passenger_id,
                    "added to the",
                    flight_id,
                    "waitlist at position",
                    position,
                    "."
                )

        return bookings, next_booking_number

    # Ask for the seat
    seat_label = input("Seat (for example 2C): ").strip().upper()

    # Check that the seat has the correct format
    if len(seat_label) != 2:
        print("Invalid seat format.")
        return bookings, next_booking_number

    if not seat_label[0].isdigit() or not seat_label[1].isalpha():
        print("Invalid seat format.")
        return bookings, next_booking_number

    # Convert the seat label into list indexes
    row_index, column_index = seat_label_to_indexes(
        seat_label,
        len(flight["seats"]),
        len(flight["seats"][0])
    )

    # Check that the seat exists on this particular flight
    if row_index is None or column_index is None:
        print("Seat is not available on this flight.")
        return bookings, next_booking_number

    # Check whether the seat is already occupied
    if flight["seats"][row_index][column_index] == "X":
        print("Seat is already occupied.")
        return bookings, next_booking_number

    # Check whether this passenger already has a booking on this flight
    existing_booking = find_passenger_booking(
        bookings,
        passenger_id,
        flight_id
    )

    if existing_booking is not None:
        print("Passenger already has a booking on this flight.")
        return bookings, next_booking_number

    # Mark the selected seat as occupied
    flight["seats"][row_index][column_index] = "X"

    # Create the new booking ID
    booking_id = "BK" + str(next_booking_number)

    # Add the booking to the bookings dictionary
    bookings[booking_id] = {
        "passenger": passenger_id,
        "flight": flight_id,
        "seat": seat_label
    }

    # Increase the booking number for the next booking
    next_booking_number += 1

    # Confirm the booking
    print(
        "Booked",
        booking_id,
        ":",
        passenger_id,
        "on",
        flight_id,
        "seat",
        seat_label,
        "| R" + format(flight["price"], ".2f")
    )

    return bookings, next_booking_number


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
    


