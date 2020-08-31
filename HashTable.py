# Jayson Valderrama
# ID: 001081738
# Data Structures and Algorithms II C950

class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = [[] for i in range(capacity)]

    # O(1)
    # Inserts a value by its hashed key
    def insert(self, key, value):
        bucket = hash(key) % self.capacity
        self.table[bucket].append(value)

    # O(1)
    # Only used for location_hash_table
    # Returns the Location ID of an address/zip via a Package's address/zip
    def search_destination_id_by_package(self, k):
        key = (k.address, k.zip_)
        bucket = hash(key) % self.capacity
        for value in self.table[bucket]:
            if (value.address, value.zip_) == key:
                return value.id_

    # O(1)
    # Only used for package_hash_table
    # Returns Package object via a Package ID
    def search_package_by_id(self, key):
        bucket = hash(key) % self.capacity
        for value in self.table[bucket]:
            if value.id_ == key:
                return value