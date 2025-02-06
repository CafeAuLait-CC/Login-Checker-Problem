#
#  cuckoo_filter.py
#  Login Checker Program
#
#  Created by Pinjing Xu on 2/3/25.
#  Copyright © 2025 Pinjing (Alex) Xu. All rights reserved.
#

import mmh3
import math
import logging


class CuckooFilter(object):
    def __init__(self, total_capacity=int(1e9), bucket_size=4, fingerprint_size=12):
        # The num of slots in each bucket
        self.bucket_size = bucket_size

        """
        Ideal num of bucket is calculated as : m = n / (a x b),
        where   m is the number of bucket;
                n is the total capacity of cuckoo filter;
                a is the load factor;
                b is the bucket size.
        For dataset large as 1 billion elements in total, 
        bucket size 4 and load factor of 95% is a ideal option to use.

        In addition, to make sure the hash calculation results in a valid index number in the range [0, bucket_num],
        we'll use a power of 2 as the bucket_num
        """
        self.load_factor = 0.8
        self.bucket_num_bit_length = int(
            math.log2(total_capacity / (self.load_factor * self.bucket_size))
        )
        self.bucket_num = 2**self.bucket_num_bit_length

        self.buckets = [[] for _ in range(self.bucket_num)]
        self.finger_bits = fingerprint_size
        self.max_kick = 900

    # Insert an username into filter
    def insert(self, username):
        h1x = self.h1(username)
        finger = self.fingerprint(username)
        res = self.insert_into(finger, h1x)
        if res is not None:
            logging.error(res + f"\nFailed with username: {username}")

    """
    Insert fingerprint into buckets
     - finger: fingerprint of element
     - idx: target index
     - counter: Use a counter to keep tracking the number of times a saved record is kicked out and moved to backup bucket.
                if the counter goes large, stop the recurrsion process and the entire filter needs to be reshuffled
    """

    def insert_into(self, finger: int, idx: int, counter=0):
        try:
            kicked_finger = None
            if not self.full(idx):
                self.buckets[idx].append(finger)
                return None
            else:
                kicked_finger = self.kick_out_move_in(idx, finger)
                h2x = self.h2(idx, kicked_finger)
                counter += 1
                if counter > self.max_kick:
                    return f"kicked too many times, failed to insert, reshuffle needed! fingerprint: {finger}; index: {idx}"
                return self.insert_into(kicked_finger, h2x, counter)
        except IndexError:
            logging.error(
                f"IndexError: length: {self.bucket_num};\
                inserting finger:{finger} into idx:{idx}, \
                possible h2x:{self.h2(idx, self.buckets[idx][0])}"
            )

    """
    Lookup for a username in the filter
     - username: the target string

    Return True if the username is found in the filter, either in the first bucket or the backup bucket. Otherwise, return False.
    """

    def exist(self, username: str):
        h1x = self.h1(username)
        finger = self.fingerprint(username)
        h2x = self.h2(h1x, finger)
        try:
            return finger in self.buckets[h1x] + self.buckets[h2x]
        except IndexError:
            logging.error(
                f"Failed to look for user: {username}. h1x:{h1x}, finger:{finger}, h2x:{h2x}, bucket_num:{self.bucket_num}"
            )
            return False

    """
    Kick out the first(oldest) fingerprint in a bucket, and insert a new one at the end.
     - idx: the index of the target bucket.
     - finger: fingerprint

     Return the oledst fingerprint that is being kicked out.
    """

    def kick_out_move_in(self, idx, finger) -> int:
        out = self.buckets[idx][0]
        self.buckets[idx][0] = self.buckets[idx][1]
        self.buckets[idx][1] = self.buckets[idx][2]
        self.buckets[idx][2] = self.buckets[idx][3]
        self.buckets[idx][3] = finger
        return out

    # Fingerprint is calculated by truncate the hash value with a bitmask of length 8 or 12
    def fingerprint(self, username: str):
        return self.h1(username) & ((1 << self.finger_bits) - 1)

    def h1(self, username: str) -> int:
        return mmh3.hash(username) % self.bucket_num

    def h2(self, h1x: int, fingerprint: int) -> int:
        hf = mmh3.hash(str(fingerprint), signed=False)
        # h1x_bit_length = h1x.bit_length()
        # hf_bit_length = hf.bit_length()
        # if hf_bit_length > h1x_bit_length:
        #     hf = hf >> (hf_bit_length - h1x_bit_length + 1)
        """
        To make sure the resulting H2 value lies within the range of [0, bucket_number],
            we use bitmask to constrain the value of H2, calculating as follows:

            H2 = (H1 xor hash(fingerprint)) & (bucket_num - 1)

        The bitmask (bucket_num - 1) effectively truncates the result of the XOR operation 
            to the number of bits required to represent bucket_num. Since num_buckets is a power of 2, 
            (num_buckets - 1) is a bitmask with all lower bits set to 1 
            (e.g., for num_buckets = 256, the bitmask is 11111111 in binary).
        Reference: https://stackoverflow.com/questions/66585651
        """
        return (h1x ^ hf) & (self.bucket_num - 1)

    # check if a bucket is full
    def full(self, idx: int):
        return len(self.buckets[idx]) == self.bucket_size

    def __str__(self):
        return f"bucket size: {self.bucket_size}\nnumber of buckets: {self.bucket_num}\nfingerprint size: {self.finger_bits}"
