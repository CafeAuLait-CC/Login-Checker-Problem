#
#  simple_algorithms.py
#  Login Checker Program
#
#  Created by Pinjing Xu on 2/5/25.
#  Copyright © 2025 Pinjing (Alex) Xu. All rights reserved.
#

from tqdm import tqdm

import time


def run_linear_search(name_list, check_list):
    print("Running demo of Linear Search...")
    counter = 0
    print("Linear Search is too slow! Force reducing the test set to 1000!")
    print("Start searching...")
    t_start = time.time()
    for name in tqdm(check_list[:1000], total=1000):
        for i in range(len(name_list)):
            if name == name_list[i]:
                counter += 1

    t_end = time.time()
    print(
        f"\nLinear Search Done! {counter}/{len(check_list)} usernames in the list already exists, \
        time consumed {t_end - t_start:.4f} seconds"
    )


def run_binary_search(name_list, check_list):
    print("Running demo of Binary Search...")
    counter = 0
    print("Start searching...")
    t_start = time.time()
    for name in tqdm(check_list, total=len(check_list)):
        if binary_search(name, name_list, 0, len(name_list) - 1):
            counter += 1
    t_end = time.time()
    print(
        f"\nBinary Search Done! {counter}/{len(check_list)} usernames in the list already exists, \
        time consumed {t_end - t_start:.4f} seconds"
    )


# Binary Search Algorithm
def binary_search(target, data, start_idx, end_idx) -> bool:
    if target > data[end_idx] or target < data[start_idx]:
        return False

    if (end_idx - start_idx) == 1:
        if data[end_idx] == target or data[start_idx] == target:
            return True
        else:
            return False
    else:
        mid = (start_idx + end_idx) // 2
        if target > data[mid]:
            start_idx = mid
            return binary_search(target, data, start_idx, end_idx)
        else:
            end_idx = mid
            return binary_search(target, data, start_idx, end_idx)


def run_hash_table(name_list, check_list):
    print("Running demo of Hash Mapping (using Python built-in dict)...")
    print("Building the hash table...")
    table = build_hash_table(name_list)

    print("Start searching...")
    counter = 0
    t_start = time.time()
    for name in check_list:
        if table.get(name) is not None:
            counter += 1
    t_end = time.time()
    print(
        f"\nHash Mapping Done! {counter}/{len(check_list)} usernames in the list already exists, \
        time consumed {t_end - t_start:.4f} seconds"
    )


def build_hash_table(keys) -> dict:
    user_dict = {}
    for key in keys:
        user_dict[key] = 1
    return user_dict
