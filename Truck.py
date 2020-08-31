# Jayson Valderrama
# ID: 001081738
# Data Structures and Algorithms II C950

from collections import defaultdict


class Truck:
    # Capacity and speed noted in project details
    CAPACITY = 16
    SPEED_MPH = 18

    def __init__(self, truck_id, clock_time):
        self.truck_id = truck_id
        self.clock_time = clock_time
        self.distance_traveled = 0
        self.packages = []
        self.delivery_locations = defaultdict(set)
        self.delivery_locations[0]

    # Packages are only added if there is remaining capacity and
    # packages are only added when a Truck leaves for deliveries
    def add_package(self, package, destination_id):
        if len(self.packages) < self.CAPACITY:
            package.status = package.OUT_FOR_DELIVERY
            self.delivery_locations[destination_id].add(package)

    # Dictionary allows multiple Packages to be assigned to a delivery location
    # Any package being dropped off is updated as delivered or delivered late
    # Delivery location then removed
    def remove_destination(self, location):
        for package in self.delivery_locations.get(location):
            if package.deadline >= self.clock_time.time():
                package.status = package.DELIVERED
            else:
                package.status = package.DELIVERED_LATE
        del self.delivery_locations[location]