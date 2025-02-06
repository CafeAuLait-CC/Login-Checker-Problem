#
#  bloom_filter.py
#  Login Checker Program
#
#  Created by Pinjing Xu on 2/1/25.
#  Copyright © 2025 Pinjing (Alex) Xu. All rights reserved.
#

from bitarray import bitarray

import mmh3
import math


class BloomFilter:
    def __init__(self, num_users=1e9, prob=0.1):
        self.probability_fp = prob
        self.size = int(
            -1 * num_users * math.log(self.probability_fp) / (math.log(2)) ** 2
        )
        self.num_hash = int(self.size / num_users * math.log(2))
        self.filter = bitarray(self.size)
        # not neccessary. bitarray() returns all zeros by itself
        self.filter.setall(0)

    def insert(self, item):
        for i in range(self.num_hash):
            digit = mmh3.hash(item, seed=i) % self.size
            self.filter[digit] = 1

    def exist(self, item):
        sum = 0
        for i in range(self.num_hash):
            digit = mmh3.hash(item, seed=i) % self.size
            if self.filter[digit] == 1:
                sum += 1
        if sum == self.num_hash:
            return True
        return False

    def __str__(self):
        return f"{self.filter}"
