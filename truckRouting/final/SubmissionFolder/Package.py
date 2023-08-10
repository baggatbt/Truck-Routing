import datetime


class Package:
    def __init__(self, package_id, delivery_address, delivery_city, delivery_state, delivery_zipcode, 
                 deadline, package_weight, delivery_status):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zipcode = delivery_zipcode
        self.deadline = deadline
        self.package_weight = package_weight
        self.delivery_status = delivery_status
        self.start_time = None
        self.arrival_time = None

    def __str__(self):
        return f"{self.package_id}, {self.delivery_address}, {self.delivery_city}, {self.delivery_state}, " \
               f"{self.delivery_zipcode}, {self.deadline}, {self.package_weight}, {self.arrival_time}, " \
               f"{self.delivery_status}"

    def update_delivery_status(self, time_stamp):
        start_of_day = datetime.datetime(time_stamp.year, time_stamp.month, time_stamp.day)
        start_datetime = start_of_day + self.start_time
        arrival_datetime = start_of_day + self.arrival_time
        if arrival_datetime <= time_stamp:
            self.delivery_status = "Delivered at " + str(arrival_datetime.time())
        elif start_datetime <= time_stamp < arrival_datetime:
            self.delivery_status = "In transit"
        else:
            self.delivery_status = "At hub"