"""
ELEVATOR SYSTEM DESIGN & SIMULATOR
FCFS (First-Come, First-Served) Scheduling
"""

from dataclasses import dataclass
from collections import deque


@dataclass
class HallCall:
    sequence: int
    floor: int
    direction: str


def ask_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Enter a value >= {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Enter a value <= {maximum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")


def ask_float(prompt, minimum=0):
    while True:
        try:
            value = float(input(prompt))
            if value < minimum:
                print(f"Enter a value >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def ask_direction():
    while True:
        choice = input(
            "Select direction (1 = UP, 2 = DOWN): "
        ).strip().lower()

        if choice in ("1", "up", "u"):
            return "UP"
        elif choice in ("2", "down", "d"):
            return "DOWN"

        print("Invalid choice. Select UP or DOWN.")


def get_configuration():
    print("\n========== ELEVATOR CONFIGURATION ==========")

    total_floors = ask_int(
        "Enter total number of floors: ", 2
    )

    starting_floor = ask_int(
        f"Enter starting floor (0-{total_floors - 1}): ",
        0,
        total_floors - 1
    )

    max_people = ask_int(
        "Maximum number of passengers allowed: ", 1
    )

    max_load = ask_float(
        "Maximum elevator load (kg): ", 1
    )

    speed = ask_float(
        "Elevator speed (floors per minute): ", 0.01
    )

    door_time = ask_float(
        "Door opening/closing time per stop (seconds): ", 0
    )

    return (
        total_floors,
        starting_floor,
        max_people,
        max_load,
        speed,
        door_time
    )


def create_calls(total_floors):
    print("\n========== REGISTER ELEVATOR CALLS ==========")

    calls = []
    sequence = 1

    while True:
        add = input(
            "\nDo you want to press an elevator button? (Y/N): "
        ).strip().lower()

        if add not in ("y", "yes"):
            break

        floor = ask_int(
            f"Enter floor for request #{sequence}: ",
            0,
            total_floors - 1
        )

        direction = ask_direction()

        if direction == "UP" and floor == total_floors - 1:
            print("The top floor has no UP button.")
            continue

        if direction == "DOWN" and floor == 0:
            print("The ground floor has no DOWN button.")
            continue

        calls.append(
            HallCall(sequence, floor, direction)
        )

        print(
            f"Request #{sequence} registered: "
            f"Floor {floor}, Direction {direction}"
        )

        sequence += 1

    return calls


def board_passengers(
    call,
    max_people,
    max_load,
    total_floors
):
    print(
        f"\nElevator arrived at floor {call.floor} "
        f"({call.direction})."
    )

    while True:
        count = ask_int(
            f"Number of passengers boarding (0-{max_people}): ",
            0,
            max_people
        )

        weights = []

        for person in range(1, count + 1):
            weight = ask_float(
                f"Enter weight of passenger {person} (kg): ",
                1
            )
            weights.append(weight)

        total_weight = sum(weights)

        if total_weight > max_load:
            print(
                f"OVERLOAD! Total weight: {total_weight:.2f} kg. "
                f"Maximum capacity: {max_load:.2f} kg."
            )
            print("Please enter a smaller passenger group.")
            continue

        break

    print(
        f"\nPassengers accepted: {count}"
        f"\nTotal passenger weight: {total_weight:.2f} kg"
        f"\nRemaining capacity: {max_load - total_weight:.2f} kg"
    )

    destinations = []

    for person in range(1, count + 1):

        while True:
            destination = ask_int(
                f"Passenger {person} destination floor: ",
                0,
                total_floors - 1
            )

            if destination == call.floor:
                print("Destination cannot be the current floor.")
                continue

            if (
                call.direction == "UP"
                and destination < call.floor
            ):
                print("Select a floor above the current floor.")
                continue

            if (
                call.direction == "DOWN"
                and destination > call.floor
            ):
                print("Select a floor below the current floor.")
                continue

            destinations.append(destination)
            break

    return count, total_weight, destinations


def run_simulation(config, calls):

    (
        floors,
        current,
        max_people,
        max_load,
        speed,
        door_time
    ) = config

    queue = deque(calls)

    total_distance = 0
    total_stops = 0
    total_time = 0

    print("\n========== ELEVATOR SIMULATION ==========")

    print(f"Starting floor: {current}")

    print("\nFCFS REQUEST QUEUE:")

    for call in calls:
        print(
            f"Request #{call.sequence}: "
            f"Floor {call.floor} - {call.direction}"
        )

    while queue:

        call = queue.popleft()

        print("\n" + "=" * 50)

        print(
            f"PROCESSING REQUEST #{call.sequence}"
        )

        print(f"Destination floor: {call.floor}")
        print(f"Requested direction: {call.direction}")

        distance = abs(call.floor - current)

        travel_time = (distance / speed) * 60

        print(
            f"\nElevator moving from floor {current} "
            f"to floor {call.floor}."
        )

        print(f"Distance: {distance} floors")
        print(f"Estimated travel time: {travel_time:.2f} seconds")

        total_distance += distance
        total_time += travel_time

        current = call.floor
        total_stops += 1

        count, weight, destinations = board_passengers(
            call,
            max_people,
            max_load,
            floors
        )

        total_time += door_time

        if count == 0:
            print("No passengers boarded.")
            continue

        print("\nPassenger destinations:", destinations)

        ordered_stops = sorted(
            set(destinations),
            reverse=(call.direction == "DOWN")
        )

        for stop in ordered_stops:

            distance = abs(stop - current)

            travel_time = (distance / speed) * 60

            total_distance += distance
            total_time += travel_time + door_time
            total_stops += 1

            print(
                f"\nElevator moving from floor {current} "
                f"to floor {stop}."
            )

            print(f"Distance: {distance} floors")
            print(f"Travel time: {travel_time:.2f} seconds")

            current = stop

            leaving = destinations.count(stop)

            print(
                f"Floor {stop}: "
                f"{leaving} passenger(s) exited."
            )

        print("\nPassenger group delivered.")
        print(f"Current elevator floor: {current}")

    print("\n========== FINAL PERFORMANCE REPORT ==========")

    print(f"Total distance travelled: {total_distance} floors")
    print(f"Total number of stops: {total_stops}")
    print(f"Final elevator position: Floor {current}")
    print(f"Total estimated time: {total_time:.2f} seconds")

    print("\nAll requests processed in FCFS order.")


def main():

    print("=" * 55)
    print("       ELEVATOR SYSTEM DESIGN AND SIMULATOR")
    print("       FIRST-COME, FIRST-SERVED METHOD")
    print("=" * 55)

    config = get_configuration()

    calls = create_calls(config[0])

    if not calls:
        print("\nNo elevator requests registered.")
        return

    run_simulation(config, calls)


if __name__ == "__main__":
    main()