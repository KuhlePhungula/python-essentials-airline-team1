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


# Cancels an existing booking and promotes the first waitlisted passenger if needed
def cancel_booking(flights, passengers, bookings, next_booking_number):

    # Ask for the booking ID
    booking_id = input("Booking ID: ").strip().upper()

    # Check whether the booking exists
    if booking_id not in bookings:
        print("Booking does not exist.")
        return bookings, next_booking_number

    # Get the booking information
    booking = bookings[booking_id]

    passenger_id = booking["passenger"]
    flight_id = booking["flight"]
    seat_label = booking["seat"]

    # Get the flight
    flight = flights[flight_id]

    # Convert the seat label into indexes
    row_index, column_index = seat_label_to_indexes(
        seat_label,
        len(flight["seats"]),
        len(flight["seats"][0])
    )

    # Free the seat
    flight["seats"][row_index][column_index] = " "

    # Remove the booking
    del bookings[booking_id]

    print(
        "Cancelled",
        booking_id,
        ":",
        passenger_id,
        "from",
        flight_id,
        "seat",
        seat_label
    )

    # Check whether anyone is waiting for this flight
    if len(flight["waitlist"]) > 0:

        # Get the first passenger in the waitlist
        waiting_passenger = flight["waitlist"][0]

        # Remove that passenger from the waitlist
        del flight["waitlist"][0]

        # Create a new booking
        new_booking_id = "BK" + str(next_booking_number)

        bookings[new_booking_id] = {
            "passenger": waiting_passenger,
            "flight": flight_id,
            "seat": seat_label
        }

        # Mark the freed seat as occupied again
        flight["seats"][row_index][column_index] = "X"

        # Increase the booking number
        next_booking_number += 1

        print(
            "Promoted",
            waiting_passenger,
            "from waitlist to",
            flight_id,
            "seat",
            seat_label,
            "as",
            new_booking_id
        )

    return bookings, next_booking_number


# Changes a passenger's existing seat on a flight
def change_seat(flights, passengers, bookings):

    # Ask for the booking ID
    booking_id = input("Booking ID: ").strip().upper()

    # Check whether the booking exists
    if booking_id not in bookings:
        print("Booking does not exist.")
        return

    # Get the booking details
    booking = bookings[booking_id]

    passenger_id = booking["passenger"]
    flight_id = booking["flight"]
    old_seat = booking["seat"]

    # Get the flight
    flight = flights[flight_id]

    # Ask for the new seat
    new_seat = input("New seat (for example 2C): ").strip().upper()

    # Check the seat format
    if len(new_seat) != 2:
        print("Invalid seat format.")
        return

    if not new_seat[0].isdigit() or not new_seat[1].isalpha():
        print("Invalid seat format.")
        return

    # Convert the new seat label into indexes
    new_row, new_column = seat_label_to_indexes(
        new_seat,
        len(flight["seats"]),
        len(flight["seats"][0])
    )

    # Check that the new seat exists
    if new_row is None or new_column is None:
        print("Seat is not available on this flight.")
        return

    # Check that the passenger isn't trying to choose their current seat
    if new_seat == old_seat:
        print("You are already booked in that seat.")
        return

    # Check whether the new seat is occupied
    if flight["seats"][new_row][new_column] == "X":
        print("Seat is already occupied.")
        return

    # Convert the old seat into indexes
    old_row, old_column = seat_label_to_indexes(
        old_seat,
        len(flight["seats"]),
        len(flight["seats"][0])
    )

    # Free the old seat
    flight["seats"][old_row][old_column] = " "

    # Occupy the new seat
    flight["seats"][new_row][new_column] = "X"

    # Update the booking
    bookings[booking_id]["seat"] = new_seat

    # Confirm the change
    print(
        "Changed",
        booking_id,
        ":",
        passenger_id,
        "from",
        old_seat,
        "to",
        new_seat
    )

    return


# Adds a passenger to a flight's waitlist
def join_waitlist(flights, passengers, flight_id, passenger_id):

    # Check that the passenger exists
    if passenger_id not in passengers:
        print("Passenger does not exist.")
        return

    # Check that the flight exists
    if flight_id not in flights:
        print("Flight does not exist.")
        return

    # Get the flight
    flight = flights[flight_id]

    # Check if the passenger is already on the waitlist
    if passenger_id in flight["waitlist"]:
        print("Passenger is already on the waitlist.")
        return

    # Add the passenger to the end of the waitlist
    flight["waitlist"].append(passenger_id)

    # Calculate their position
    position = len(flight["waitlist"])

    # Confirm the waitlist position
    print(
        passenger_id,
        "added to the",
        flight_id,
        "waitlist at position",
        position
    )

    return position


# Promotes the first passenger from the waitlist into a newly available seat
def promote_from_waitlist( flights, passengers, bookings, flight_id, seat_label, next_booking_number ):

    # Check that the flight exists
    if flight_id not in flights:
        print("Flight does not exist.")
        return bookings, next_booking_number

    # Get the flight
    flight = flights[flight_id]

    # Check whether there is anyone waiting
    if len(flight["waitlist"]) == 0:
        return bookings, next_booking_number

    # Get the first passenger in the waitlist
    passenger_id = flight["waitlist"][0]

    # Remove the passenger from the waitlist
    del flight["waitlist"][0]

    # Convert the seat label into indexes
    row_index, column_index = seat_label_to_indexes(
        seat_label,
        len(flight["seats"]),
        len(flight["seats"][0])
    )

    # Mark the seat as occupied
    flight["seats"][row_index][column_index] = "X"

    # Create a new booking ID
    booking_id = "BK" + str(next_booking_number)

    # Add the new booking
    bookings[booking_id] = {
        "passenger": passenger_id,
        "flight": flight_id,
        "seat": seat_label
    }

    # Increase the booking number
    next_booking_number += 1

    # Get the passenger's name
    passenger_name = passengers[passenger_id]["name"]

    # Print the promotion confirmation
    print(
        "Promoted",
        passenger_id,
        "-",
        passenger_name,
        "from waitlist to",
        flight_id,
        seat_label,
        "as",
        booking_id
    )

    return bookings, next_booking_number


# Displays all booked passengers for a flight in seat order
def flight_manifest(flights, passengers, bookings):

    # Ask for the flight ID
    flight_id = input("Flight ID: ").strip().upper()

    # Check that the flight exists
    if flight_id not in flights:
        print("Flight does not exist.")
        return

    # Get the selected flight
    flight = flights[flight_id]

    # Keep track of bookings for this flight
    flight_bookings = []

    # Find all bookings belonging to this flight
    for booking_id in bookings:
        booking = bookings[booking_id]

        if booking["flight"] == flight_id:
            flight_bookings.append(booking_id)

    # Display the manifest heading
    print("\n--- Flight Manifest ---")
    print(
        flight_id,
        "|",
        flight["origin"],
        "->",
        flight["dest"]
    )

    # Check whether there are any bookings
    if len(flight_bookings) == 0:
        print("No passengers booked.")
    else:

        # Display each booking
        for booking_id in flight_bookings:

            booking = bookings[booking_id]
            passenger_id = booking["passenger"]
            seat_label = booking["seat"]

            passenger_name = passengers[passenger_id]["name"]

            print(
                booking_id,
                "|",
                passenger_id,
                "|",
                passenger_name,
                "|",
                seat_label
            )

    # Display the waitlist
    print("Waitlist:")

    if len(flight["waitlist"]) == 0:
        print("(waitlist empty)")
    else:
        position = 1

        for passenger_id in flight["waitlist"]:

            passenger_name = passengers[passenger_id]["name"]

            print(
                position,
                "|",
                passenger_id,
                "|",
                passenger_name
            )

            position += 1

    return


# Displays revenue and occupancy information for every flight
def revenue_report(flights, bookings):

    print("\n--- Revenue Report ---")

    total_revenue = 0
    fullest_flight = None
    highest_occupancy = -1
    total_waitlisted = 0

    # Go through every flight
    for flight_id in flights:

        flight = flights[flight_id]

        # Count seats
        taken, total = seat_counts(flight["seats"])

        # Calculate occupancy percentage
        if total > 0:
            occupancy = (taken / total) * 100
        else:
            occupancy = 0

        # Calculate revenue for this flight
        revenue = calculate_flight_revenue(
            bookings,
            flight_id,
            flight["price"]
        )

        # Count people waiting
        waitlisted = len(flight["waitlist"])

        # Add to academy totals
        total_revenue += revenue
        total_waitlisted += waitlisted

        # Check whether this is the fullest flight
        if occupancy > highest_occupancy:
            highest_occupancy = occupancy
            fullest_flight = flight_id

        # Display the flight's information
        print(
            flight_id,
            "|",
            flight["origin"],
            "->",
            flight["dest"],
            "|",
            str(taken) + "/" + str(total),
            "|",
            format(occupancy, ".1f") + "%",
            "|",
            "R" + format(revenue, ".2f")
        )

    # Display academy totals
    print("\n--- Academy Totals ---")
    print(
        "Total revenue: R" + format(total_revenue, ".2f")
    )
    print(
        "Fullest flight:",
        fullest_flight
    )
    print(
        "Total waitlisted:",
        total_waitlisted
    )

    return


# Finds an existing booking for a passenger on a specific flight
def find_passenger_booking(bookings, passenger_id, flight_id):
    for booking_id in bookings:
        booking = bookings[booking_id]

        if booking["passenger"] == passenger_id and booking["flight"] == flight_id:
            return booking_id

    return None


# returns a single flight's revenue
def calculate_flight_revenue(flight):
    taken, total = seat_counts(flight["seats"])
    revenue = taken * flight["price"]
    return revenue, taken, total 


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
    


