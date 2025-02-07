#
#  test_cuckoo_filter.py
#  Login Checker Program
#
#  Created by Generative AI (DeepSeek) on 2/4/25.
#

import unittest

from src.cuckoo_filter import CuckooFilter


class TestCuckooFilter(unittest.TestCase):
    def setUp(self):
        """Initialize the Cuckoo Filter for testing."""
        self.cf = CuckooFilter(capacity=100, bucket_size=4, fingerprint_size=8)

    def test_fingerprint(self):
        """Test if the fingerprint is calculated correctly."""
        username = "hello_wo"
        expected_fingerprint = self.cf.h1(username) & ((1 << self.cf.finger_bits) - 1)
        self.assertEqual(self.cf.fingerprint(username), expected_fingerprint)

    def test_h1(self):
        """Test if h1 produces a valid bucket index."""
        username = "hello_wo"
        h1x = self.cf.h1(username)
        self.assertTrue(0 <= h1x < self.cf.bucket_num)

    def test_h2(self):
        """Test if h2 produces a valid bucket index."""
        username = "hello_wo"
        h1x = self.cf.h1(username)
        fingerprint = self.cf.fingerprint(username)
        h2x = self.cf.h2(h1x, fingerprint)
        self.assertTrue(0 <= h2x < self.cf.bucket_num)

    def test_insert(self):
        """Test insertion of elements into the filter."""
        username = "hello_wo"
        self.cf.insert(username)
        h1x = self.cf.h1(username)
        fingerprint = self.cf.fingerprint(username)
        self.assertIn(fingerprint, self.cf.buckets[h1x])

    def test_kick_out(self):
        """Test kicking out elements when a bucket is full."""
        # Create a new username
        username = "hello_wo"

        # Fill a bucket to its capacity
        bucket_idx = self.cf.h1(username)
        for i in range(self.cf.bucket_size):
            self.cf.buckets[bucket_idx].append(i)  # Fill with dummy fingerprints

        # Insert the new element into the full bucket
        self.cf.insert(username)

        # Check if the new fingerprint is in the bucket
        fingerprint = self.cf.fingerprint(username)
        self.assertTrue(
            fingerprint in self.cf.buckets[bucket_idx]
            or fingerprint in self.cf.buckets[self.cf.h2(bucket_idx, fingerprint)]
        )

    def test_full(self):
        """Test if the full method correctly identifies a full bucket."""
        bucket_idx = 0
        for i in range(self.cf.bucket_size):
            self.cf.buckets[bucket_idx].append(i)  # Fill with dummy fingerprints
        self.assertTrue(self.cf.full(bucket_idx))

    def test_kick_out_too_many_times(self):
        """Test if the filter handles excessive kicking out."""
        # Fill all buckets to force excessive kicking
        for bucket in self.cf.buckets:
            for i in range(self.cf.bucket_size):
                bucket.append(i)  # Fill with dummy fingerprints

        # Try to insert a new element
        username = "hello_wo"
        with self.assertLogs(level="INFO") as log:
            self.cf.insert(username)
            self.assertIn("kicked too many times", log.output[0])

    def test_exist(self):
        """Test if the exist function correctly identifies whether a username is in the filter."""
        # Insert a username into the filter
        username = "hello_wo"
        self.cf.insert(username)

        # Check if the username exists in the filter
        self.assertTrue(self.cf.exist(username))

        # Check for a username that was not inserted
        non_existent_username = "non_existent_username"
        self.assertFalse(self.cf.exist(non_existent_username))

        # Insert multiple usernames and check their existence
        usernames = ["user1", "user2", "user3"]
        for user in usernames:
            self.cf.insert(user)
            self.assertTrue(self.cf.exist(user))

        # Check for a username that was kicked out
        # Fill a bucket to force kicking out
        bucket_idx = None
        for i in range(self.cf.bucket_size):
            user = f"user_{i}"
            self.cf.insert(user)
            h1x = self.cf.h1(user)
            if bucket_idx is None:
                bucket_idx = h1x  # Track the first bucket index

        # Insert one more username to trigger kicking out
        kicked_user = "kicked_user"
        self.cf.insert(kicked_user)

        # Check if the kicked-out username still exists in the filter
        self.assertTrue(self.cf.exist(kicked_user))

        # Check if the first inserted username in the bucket still exists
        first_user = "user_0"
        self.assertTrue(self.cf.exist(first_user))


if __name__ == "__main__":
    unittest.main()
