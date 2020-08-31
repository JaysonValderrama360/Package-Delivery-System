# Jayson Valderrama
# ID: 001081738
# Data Structures and Algorithms II C950

from datetime import time, datetime


class Package:
    # Package statuses
    AT_FACILITY = "At Facility"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    DELIVERED_LATE = "Delivered Late"

    # Manually defined End of Day as 5pm
    EOD_HOUR = 17
    EOD_MIN = 00

    # These packages are marked as a bundle via the project constraints
    BUNDLED_PACKAGES = [13, 14, 15, 16, 19, 20]

    # Package initialization
    def __init__(self, id_, address, city, state, zip_, deadline, kilos, note):
        self.id_ = int(id_)
        self.address = address
        self.city = city
        self.state = state
        self.zip_ = zip_
        self.deadline = deadline
        self.kilos = kilos
        self.note = note
        self.status = self.AT_FACILITY
        self.bundled = False
        self.truck_id = None

        # Updates package's delivery deadline to "time" object
        if self.deadline == "EOD":
            self.deadline = time(self.EOD_HOUR, self.EOD_MIN)
        else:
            self.deadline = datetime.strptime(self.deadline[0:5].strip(), "%H:%M").time()

        if note != '' or None:
            # Updates as True if a package is bundled
            if self.id_ in self.BUNDLED_PACKAGES:
                self.bundled = True

            # Assigns the Truck ID 2 if package requires it
            elif self.note[-7:] == "truck 2":
                self.truck_id = 2

            # Updates status of delayed packages
            elif self.note[0:7] == "Delayed":
                self.arrive_time = self.note[-7:-3]

            # Updates incorrect address
            elif self.note == "Wrong address listed":
                self.address = "410 S State St"
                self.zip_ = "84111"

    # Formatted Package display when called in Main
    def __str__(self):
        return '{:<5}'.format(str(self.id_)) + \
               '{:<41}'.format(self.address) + \
               '{:<19}{:<8}{:<8}'.format(self.city, self.state, self.zip_) + \
               '{}'.format( self.deadline) + \
               '{:>8}{:<3}'.format(self.kilos, '') + \
               '{:<19}'.format(self.status) + \
               '{}'.format(self.note)
