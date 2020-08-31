# Jayson Valderrama
# ID: 001081738
# Data Structures and Algorithms II C950


from DeliverySystem import DeliverySystem
from Truck import Truck
from Package import Package
import datetime


if __name__ == "__main__":
    # Manually sorted package bundles. Meets the constraints laid out by the Package File and the assignment
    # rubric, but not optimized any further. Package bundles are assigned to one of the three trucks, following
    # the constraints, and the trucks leave and return at times required of the bundles.
    first_bundle = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
    second_bundle = [2, 3, 4, 5, 6, 7, 8, 18, 25, 28, 32, 36, 38]
    third_bundle = [9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35, 39]
    all_packages = range(1, 41)

    # Delivery System object for package handling and truck routing
    ds = DeliverySystem()

    # "Home screen" of WGUPS that can be returned to on user input
    def greeting():
        print("\n┌─┬──────────────────────────────────────────────────┬─┐\n"
              "                    WGUPS Interface\n"
              "           Enter a number to choose a command\n\n"
              "     69 - Quit program\n"
              "     0 - View, return to home screen (use any time)\n"
              "     1 - View all packages at an exact time\n"
              "     2 - View a package at an exact time via its ID\n"
              "     3 - View truck routes and mileage\n"
              "└─┴──────────────────────────────────────────────────┴─┘\n")
    greeting()

    # Displays the truck routes of each truck, from Location ID to Location ID; displays the clock time
    # and current mileage of each truck route segment; and displays total mileage of all trucks combined.
    def view_truck_routes():
        now = datetime.datetime.now()
        print("\n\t▪■▪ TRUCK ONE ▪■▪\nClock Time   Miles   Location ID Path")
        truck1 = ds.truck_routes(Truck(1, now.replace(hour=8, minute=0, second=0)), first_bundle)
        print("\n\t▪■▪ TRUCK TWO ▪■▪\nClock Time   Miles   Location ID Path")
        truck2 = ds.truck_routes(Truck(2, now.replace(hour=9, minute=5, second=0)), second_bundle)
        print("\n\t▪■▪ TRUCK THREE ▪■▪\nClock Time   Miles   Location ID Path")
        truck3 = ds.truck_routes(Truck(3, now.replace(hour=10, minute=0, second=0)), third_bundle)
        print("\n🚚 ID     MILEAGE\n\t1\t\t", truck1, "\n\t2\t\t", truck2, "\n\t3\t\t", truck3,
              "\n           ", truck1+truck2+truck3, end=" TOTAL\n\n")

    # Handles package bundles. Displays all package info, including the status, at supplied time.
    def view_package_bundle(text, bundle, time):
        h, m, s = time
        now = datetime.datetime.now()

        # Truck IDs are indicated by the first parameter in the Truck object, and their leaving time
        # has been pre-calculated to fit the constraints of the project. check_time is derived from
        # user input to stop a Truck during the greedy algorithm comparisons.
        check_time = now.replace(hour=h, minute=m, second=s)
        ds.package_delivery(Truck(1, now.replace(hour=8, minute=0, second=0)), first_bundle, check_time)
        ds.package_delivery(Truck(2, now.replace(hour=9, minute=5, second=0)), second_bundle, check_time)
        ds.package_delivery(Truck(3, now.replace(hour=10, minute=0, second=0)), third_bundle, check_time)

        # Prints package information
        print("\n\t▪■▪", text, check_time.strftime("%H:%M:%S"), "▪■▪")
        print("{:<5}{:<41}{:<19}{:<8}{:<8}{:<11}{:<8}{:<19}{}".format(
                "ID", "Address", "City", "State", "Zip", "Deadline", "Kilos", "Status", "Note"))
        for id_ in bundle:
            package = ds.package_hash_table.search_package_by_id(id_)
            print(package)
            # Resets package status to default
            package.status = Package.AT_FACILITY
        print()

    # Handles a single Package ID input and sends it to the main package handler function
    def view_package_by_id(package_id):
        time = time_input()
        if time != "0":
            view_package_bundle("PACKAGE VIEW AT", [int(package_id)], time)

    # Handles command-line instances when a time is required
    def time_input():
        print("\nInput time in format HH:MM:SS\n► ", end="")
        while True:
            time_input = input("")
            try:
                if time_input == "0":
                    return time_input
                h, m, s = map(int, time_input.split(':'))
                break
            except ValueError:
                print("\nTry again in a format like \"9:05:00\", or enter 0 to go home\n► ", end="")
        return h, m, s

    # Command-line interface for user input
    while True:
        user_input_A = input("Home\n► ")
        if user_input_A == "66":
            break
        if user_input_A == "0":
            greeting()
        if user_input_A == "1":
            while True:
                user_input_B = input("\n1 - Sort by ID\n2 - Sort by Truck\n► ")
                if user_input_B == "0":
                    greeting()
                    break
                if user_input_B == "1":
                    time = time_input()
                    if time == "0":
                        greeting()
                        break
                    else:
                        view_package_bundle("ALL PACKAGES AT", all_packages, time)
                        break
                if user_input_B == "2":
                    time = time_input()
                    if time == "0":
                        greeting()
                        break
                    else:
                        view_package_bundle("TRUCK 1 PACKAGES AT", first_bundle, time)
                        view_package_bundle("TRUCK 2 PACKAGES AT", second_bundle, time)
                        view_package_bundle("TRUCK 3 PACKAGES AT", third_bundle, time)
                        break
        if user_input_A == "2":
            user_input_B = input("\nEnter package ID\n► ")
            if user_input_B == "0":
                greeting()
            else:
                view_package_by_id(user_input_B)
        if user_input_A == "3":
            view_truck_routes()