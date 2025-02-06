import mmh3


class CuckooFilter:
    def __init__(self, capacity, bucket_size=4, fingerprint_size=8, max_kicks=500):
        """
        Initialize the Cuckoo Filter.

        :param capacity: Maximum number of elements the filter can hold.
        :param bucket_size: Number of entries per bucket.
        :param fingerprint_size: Number of bits for the fingerprint.
        :param max_kicks: Maximum number of kicks before reshuffling.
        """
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.fingerprint_size = fingerprint_size
        self.max_kicks = max_kicks

        # Calculate the number of buckets
        self.num_buckets = (capacity + bucket_size - 1) // bucket_size
        self.buckets = [[] for _ in range(self.num_buckets)]

        # Mask to constrain fingerprints to the desired size
        self.fingerprint_mask = (1 << fingerprint_size) - 1

    def _hash(self, item):
        """Hash function to compute the first bucket index."""
        return mmh3.hash(item) % self.num_buckets

    def _fingerprint(self, item):
        """Compute the fingerprint of an item."""
        return mmh3.hash(item) & self.fingerprint_mask

    def _alternate_bucket(self, bucket_index, fingerprint):
        """Compute the alternate bucket index using XOR."""
        return (bucket_index ^ mmh3.hash(str(fingerprint))) % self.num_buckets

    def insert(self, item):
        """
        Insert an item into the Cuckoo Filter.

        :param item: The item to insert.
        :return: True if the item was inserted successfully, False otherwise.
        """
        fingerprint = self._fingerprint(item)
        bucket_index = self._hash(item)

        # Try inserting into the primary bucket
        if self._insert_into_bucket(bucket_index, fingerprint):
            return True

        # Try inserting into the alternate bucket
        alt_bucket_index = self._alternate_bucket(bucket_index, fingerprint)
        if self._insert_into_bucket(alt_bucket_index, fingerprint):
            return True

        # If both buckets are full, perform kicking out
        for _ in range(self.max_kicks):
            # Kick out a random fingerprint from the primary bucket
            kicked_fingerprint = self.buckets[bucket_index].pop(0)
            self.buckets[bucket_index].append(fingerprint)

            # Compute the alternate bucket for the kicked fingerprint
            bucket_index = self._alternate_bucket(bucket_index, kicked_fingerprint)
            fingerprint = kicked_fingerprint

            # Try inserting the kicked fingerprint into its alternate bucket
            if self._insert_into_bucket(bucket_index, fingerprint):
                return True

        # If max kicks is reached, reshuffle the filter
        self._reshuffle()
        return self.insert(item)  # Retry insertion after reshuffling

    def _insert_into_bucket(self, bucket_index, fingerprint):
        """
        Insert a fingerprint into a bucket if it has space.

        :param bucket_index: The index of the bucket.
        :param fingerprint: The fingerprint to insert.
        :return: True if the insertion was successful, False otherwise.
        """
        if len(self.buckets[bucket_index]) < self.bucket_size:
            self.buckets[bucket_index].append(fingerprint)
            return True
        return False

    def exist(self, item):
        """
        Check if an item exists in the Cuckoo Filter.

        :param item: The item to check.
        :return: True if the item exists, False otherwise.
        """
        fingerprint = self._fingerprint(item)
        bucket_index = self._hash(item)

        # Check the primary bucket
        if fingerprint in self.buckets[bucket_index]:
            return True

        # Check the alternate bucket
        alt_bucket_index = self._alternate_bucket(bucket_index, fingerprint)
        if fingerprint in self.buckets[alt_bucket_index]:
            return True

        return False

    def _reshuffle(self):
        """Reshuffle the filter by reinserting all elements."""
        print("Reshuffling the filter...")
        all_items = []
        for bucket in self.buckets:
            all_items.extend(bucket)
        self.buckets = [[] for _ in range(self.num_buckets)]
        for fingerprint in all_items:
            self.insert(str(fingerprint))  # Reinsert fingerprints

    def __str__(self):
        """String representation of the Cuckoo Filter."""
        return f"Cuckoo Filter: {self.buckets}"


# Example usage
if __name__ == "__main__":
    cf = CuckooFilter(capacity=100, bucket_size=4, fingerprint_size=8, max_kicks=500)

    # Insert items
    items = ["hello", "world", "foo", "bar"]
    for item in items:
        cf.insert(item)

    # Check if items exist
    for item in items:
        print(f"'{item}' exists: {cf.exist(item)}")

    # Check non-existent items
    print(f"'baz' exists: {cf.exist('baz')}")
    print(f"'qux' exists: {cf.exist('qux')}")
