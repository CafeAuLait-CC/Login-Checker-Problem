#
#  test_bloom_filter.py
#  Login Checker Program
#
#  Created by Generative AI (DeepSeek) on 2/5/25.
#

import unittest
import math

from src.bloom_filter import BloomFilter


class TestBloomFilter(unittest.TestCase):
    def setUp(self):
        """Initialize the Bloom Filter for testing."""
        self.bf = BloomFilter(num_users=1000, prob=0.1)

    def test_insert_and_exist(self):
        """Test insertion and existence check for elements."""
        # Insert elements
        elements = ["hello", "world", "foo", "bar"]
        for element in elements:
            self.bf.insert(element)

        # Check if inserted elements exist
        for element in elements:
            self.assertTrue(self.bf.exist(element))

        # Check for non-inserted elements
        non_existent_elements = ["baz", "qux"]
        for element in non_existent_elements:
            self.assertFalse(self.bf.exist(element))

    def test_false_positive_rate(self):
        """Test if the false positive rate is within the expected range."""
        # Insert elements
        num_inserted = 1000
        for i in range(num_inserted):
            self.bf.insert(f"item_{i}")

        # Check for non-inserted elements
        num_tests = 10000
        false_positives = 0
        for i in range(num_inserted, num_inserted + num_tests):
            if self.bf.exist(f"item_{i}"):
                false_positives += 1

        # Calculate the observed false positive rate
        observed_fp_rate = false_positives / num_tests
        print(f"Observed false positive rate: {observed_fp_rate}")

        # Check if the observed false positive rate is within 10% of the expected rate
        expected_fp_rate = 0.1
        self.assertAlmostEqual(observed_fp_rate, expected_fp_rate, delta=0.02)

    def test_filter_size_and_hash_functions(self):
        """Test if the filter size and number of hash functions are calculated correctly."""
        num_users = 1000
        prob = 0.1
        bf = BloomFilter(num_users=num_users, prob=prob)

        # Expected filter size
        expected_size = int(-1 * num_users * math.log(prob) / (math.log(2)) ** 2)
        self.assertEqual(bf.size, expected_size)

        # Expected number of hash functions
        expected_num_hash = int(bf.size / num_users * math.log(2))
        self.assertEqual(bf.num_hash, expected_num_hash)


if __name__ == "__main__":
    unittest.main()
