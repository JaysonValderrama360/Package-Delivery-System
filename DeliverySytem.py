# Jayson Valderrama
# ID: 001081738
# Data Structures and Algorithms II C950

from HashTable import HashTable
from Package import Package
from Location import Location
from datetime import timedelta
import csv


class DeliverySystem:
    # An arbitrary reference number for the greedy algorithm's initial comparison of path lengths
    # Must be sufficiently large enough that no path the algorithm takes would come close to it
    LARGE_NUMBER = 99999

    def __init__(self):
        # O(n)
        # Loads table of distances into a hash table
        with open("WGUPS Location Table.csv") as location_file:
            location_reader = csv.reader(location_file, delimiter=',')
            self.location_hash_table = HashTable(37)
            for row in location_reader:
                location = Location(*row)
                self.location_hash_table.insert((location.address, location.zip_), location)

        # O(n²)
        # Loads all pairs of locations and puts one of the two into a dictionary
        with open("WGUPS Distance Table.csv") as distance_file:
            distance_reader = csv.reader(distance_file, delimiter=',')
            nodes = [distance for distance in distance_reader]
            self.dist_dict = {}
            for i, u in enumerate(nodes):
                for j, v in enumerate(nodes):
                    if j > i:
                        self.dist_dict[(i, j)] = float(v[i])
                        # print(i, j, '\t', v[i])

        # O(n)
        # Loads table of packages into a hash table
        with open("WGUPS Package File.csv", encoding="utf-8-sig") as package_file:
            package_reader = csv.reader(package_file, delimiter=',')
            self.package_hash_table = HashTable(53)
            for row in package_reader:
                package = Package(*row)
                self.package_hash_table.insert(package.id_, package)

    def package_delivery(self, truck, bundle, check_time):
        # On each path taken, the appropriate amount of time is added to the Truck object's clock_time
        # If it exceeds user-input check_time, the function ends in order to view package statuses
        if truck.clock_time > check_time:
            return

        # Adds to truck the package and destination via hash table lookups in O(1) time
        for id_ in bundle:
            package = self.package_hash_table.search_package_by_id(id_)
            destination_id = self.location_hash_table.search_destination_id_by_package(package)
            truck.add_package(package, destination_id)

        # O(n²)
        # This is a greedy algorithm
        def greedy_choice(node=0):
            distance = self.LARGE_NUMBER

            # A node is considered visited when it is removed from delivery locations
            truck.remove_destination(node)
            while truck.clock_time < check_time:
                # Loops through all remaining nodes and chooses the path with the shortest distance
                for neighbor_node in truck.delivery_locations:
                    temp = self.dist_dict.get((node, neighbor_node)) or self.dist_dict.get((neighbor_node, node))
                    if temp < distance:
                        distance = temp
                        next_node = neighbor_node

                # If "distance" is unchanged or abnormally large, all other paths have
                # been exhausted and the final path taken is to the starting node.
                if distance < self.LARGE_NUMBER:
                    truck.clock_time += timedelta(seconds=(distance / truck.SPEED_MPH) * 3600)

                    greedy_choice(next_node)
                else:
                    distance = self.dist_dict.get((node, 0)) or self.dist_dict.get((0, node))
                    truck.clock_time += timedelta(seconds=(distance / truck.SPEED_MPH) * 3600)
                return truck.distance_traveled
        greedy_choice()

    def truck_routes(self, truck, bundle):
        # Adds to truck the package and destination via hash table lookups in O(1) time
        for id_ in bundle:
            package = self.package_hash_table.search_package_by_id(id_)
            destination_id = self.location_hash_table.search_destination_id_by_package(package)
            truck.add_package(package, destination_id)

        # Computes and prints clock time and mileage of truck
        def greedy_helper(distance, node, next_node):
            truck.clock_time += timedelta(seconds=(distance / truck.SPEED_MPH) * 3600)
            truck.distance_traveled += distance
            truck.distance_traveled = round(truck.distance_traveled, 2)
            print(truck.clock_time.strftime('%H:%M:%S'), "   ", truck.distance_traveled, "\t", node,
                  " \t->    ", next_node)

        # O(n²)
        # This is a greedy algorithm
        def greedy_choice(node=0):
            distance = self.LARGE_NUMBER

            # A node is considered visited when it is removed from delivery locations
            truck.remove_destination(node)

            # Loops through all remaining nodes and chooses the path with the shortest distance
            for neighbor_node in truck.delivery_locations:
                temp = self.dist_dict.get((node, neighbor_node)) or self.dist_dict.get((neighbor_node, node))
                if temp < distance:
                    distance = temp
                    next_node = neighbor_node

            # If "distance" is unchanged or abnormally large, all other paths have
            # been exhausted and the final path taken is to the starting node.
            if distance < self.LARGE_NUMBER:
                greedy_helper(distance, node, next_node)
                greedy_choice(next_node)
            else:
                distance = self.dist_dict.get((node, 0)) or self.dist_dict.get((0, node))
                greedy_helper(distance, node, 0)
            return truck.distance_traveled
        return greedy_choice()
