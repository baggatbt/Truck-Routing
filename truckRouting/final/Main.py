#Brandon Baggatta
#WGU Student ID: 001251176

import csv
import datetime
from Truck import Truck
from Package import Package
from CreateHash import CreateHash

# Parse CSV files into lists
def parse_csv(file):
    with open(file) as f:
        data = list(csv.reader(f))
    return data

# Fetch CSV data
distance_data = parse_csv("Distance_File.csv")
address_data = parse_csv("Address_File.csv")
package_data = parse_csv("Package_File.csv")

# Load package data into hashtable
def package_loader(filename, package_hashtable):
    with open(filename) as package_file:
        data = csv.reader(package_file)
        for row in data:
            package_id, delivery_address, delivery_city, delivery_state, delivery_zipcode, deadline, package_weight, delivery_status = int(row[0]), *row[1:7], "At Hub"
            # Create Package object
            package = Package(package_id, delivery_address, delivery_city, delivery_state, delivery_zipcode, deadline, package_weight, delivery_status)
            # Add package to hashtable
            package_hashtable.add(package_id, package)

# Compute distance between two points
def compute_distance(point1, point2):
    dist = distance_data[point1][point2]
    if dist == '':
        dist = distance_data[point2][point1]
    return float(dist)

# Get address ID
def get_address_id(address):
    for row in address_data:
        if address in row[2]:
            return int(row[0])

# Define trucks
truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(16, 18, None, [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Initialize hashtable and load package data
package_hashtable = CreateHash()
package_loader("Package_File.csv", package_hashtable)

# Execute package delivery
def deliver(truck):
    # Prepare packages for delivery
    pending_packages = [package_hashtable.get(id) for id in truck.packages]
    truck.packages.clear()

    # Perform delivery
    while pending_packages:
        next_distance = 2000
        next_package = None
        for package in pending_packages:
            current_distance = compute_distance(get_address_id(truck.address), get_address_id(package.delivery_address))
            if current_distance <= next_distance:
                next_distance = current_distance
                next_package = package

        # Update truck status
        truck.packages.append(next_package.package_id)
        pending_packages.remove(next_package)
        truck.mileage += next_distance
        truck.address = next_package.delivery_address
        truck.time += datetime.timedelta(hours=next_distance / 18)

        # Update package status
        next_package.arrival_time = truck.time
        next_package.start_time = truck.depart_time

# Function to update delivery status for all packages
def update_all_delivery_status(time_stamp):
    for i in range(1, len(package_data)+1):  # Assuming package ids are from 1 to N
        package = package_hashtable.get(i)
        package.update_delivery_status(time_stamp)

# Function to get total mileage of all trucks
def total_truck_mileage(trucks):
    return sum(truck.mileage for truck in trucks)

# Function for user interface
def user_interface():
    while True:
        print("\n1. View the status and info of any package at any time.")
        print("2. View the total mileage traveled by all trucks.")
        print("3. View the status of all packages at a specific time.")
        print("4. Exit")

        user_choice = input("\nPlease select an option: ")

        if user_choice == '1':
            package_id = input("Enter package ID: ")
            time_str = input("Enter the time (in HH:MM format): ")
            time_obj = datetime.datetime.strptime(time_str, "%H:%M")
            package = package_hashtable.get(int(package_id))
            if package is not None:
                package.update_delivery_status(time_obj)
                print(package)

        elif user_choice == '2':
            print(f"Total Mileage: {total_truck_mileage([truck1, truck2, truck3])} miles")

        elif user_choice == '3':
            time_str = input("Enter the time (in HH:MM format): ")
            time_obj = datetime.datetime.strptime(time_str, "%H:%M")
            for package_id in range(1, 41):  # assuming 40 packages
                package = package_hashtable.get(package_id)
                if package is not None:
                    package.update_delivery_status(time_obj)
                    print(package)

        elif user_choice == '4':
            break

        else:
            print("Invalid option, please try again.")

# Begin package delivery
deliver(truck1)
deliver(truck2)
truck3.depart_time = min(truck1.time, truck2.time)
deliver(truck3)

# Start the user interface
user_interface()