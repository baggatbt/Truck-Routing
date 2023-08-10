class CreateHash:
    def __init__(self, size=20):
        self.table = [[] for _ in range(size)]

    def add(self, key, value):  # Method to insert or update an item
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket[i] = [key, value]
                return True

        bucket.append([key, value])
        return True

    def get(self, key):  # Method to retrieve an item
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]

        return None  # If key is not found

    def remove(self, key):  # Method to delete an item
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                return True

        return False  # If key is not found
