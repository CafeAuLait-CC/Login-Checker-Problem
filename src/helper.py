#
#  helper.py
#  Login Checker Program
#
#  Created by Pinjing Xu on 2/5/25.
#  Copyright © 2025 Pinjing (Alex) Xu. All rights reserved.
#

from tqdm import tqdm

from src.bloom_filter import BloomFilter
from src.cuckoo_filter import CuckooFilter
from src.cuckoo_filter_ai import CuckooFilter as CuckooFilterAI

import pickle
import time

DATA_DIR = "data/"
SORTED_USERNAMES_FILE = DATA_DIR + "sorted_usernames.txt"
USERNAMES_CHECK_FILE = DATA_DIR + "usernames_check.txt"
SAVED_BLOOM_FILTER = DATA_DIR + "prebuild/saved_bloom_filter.pkl"
SAVED_CUCKOO_FILTER = DATA_DIR + "prebuild/saved_cuckoo_filter.pkl"


def resamble_filename(src: str, dataset_postfix, ai=False):
    parts = src.split(".")
    if ai:
        dataset_postfix += "AI"
    return parts[0] + dataset_postfix + "." + parts[1]


def build_bloom_filter_from_file(filename):
    print("Initializing...")
    total = num_line(filename)
    print("Building Bloom Filter from file", filename)
    bloom_filter = BloomFilter(prob=0.05)

    # Insert data into filter
    with open(filename, "r") as f:
        for line in tqdm(f, total=total):
            bloom_filter.insert(line.strip())

    # Save data structure onto local disk as binary file for future use
    print(
        "Saving binary into ",
        resamble_filename(
            SAVED_BLOOM_FILTER, "_" + filename.split("_")[2].split(".")[0]
        ),
    )
    with open(
        resamble_filename(
            SAVED_BLOOM_FILTER, "_" + filename.split("_")[2].split(".")[0]
        ),
        "wb",
    ) as output_file:
        pickle.dump(bloom_filter, output_file)


def build_cuckoo_filter_from_file(filename, use_ai=False):
    print("Initializing (this may take a while)...")
    total = num_line(filename)
    print("Building Cuckoo Filter from file", filename)
    cuckoo_filter = None
    if use_ai:
        cuckoo_filter = CuckooFilterAI(
            capacity=int(total * 5), bucket_size=8, fingerprint_size=12
        )
    else:
        cuckoo_filter = CuckooFilter(
            capacity=int(total * 5), bucket_size=8, fingerprint_size=12
        )

    # Insert data into filter
    success = False
    while not success:
        with open(filename, "r") as f:
            for line in tqdm(f, total=total):
                success = cuckoo_filter.insert(line.strip())
                if not success:
                    # reshuffle
                    print("reshuffling...")
                    cuckoo_filter.reset()
                    break

    # Save data structure onto local disk as binary file for future use
    print(
        "Saving binary into ",
        resamble_filename(
            SAVED_CUCKOO_FILTER, "_" + filename.split("_")[2].split(".")[0], use_ai
        ),
    )
    with open(
        resamble_filename(
            SAVED_CUCKOO_FILTER, "_" + filename.split("_")[2].split(".")[0], use_ai
        ),
        "wb",
    ) as output_file:
        pickle.dump(cuckoo_filter, output_file)


def load_filter_from_disk(filename):
    print("- Loading data from", filename)
    with open(filename, "rb") as f:
        return pickle.load(f)


def check_usernames(filter, check_filename):
    print("- Looking for usernames in filter")
    with open(check_filename, "r") as f:
        check_name_list = [line.strip() for line in f.readlines()]
        counter = 0
        t_start = time.time()
        for username in check_name_list:
            if filter.exist(username):
                counter += 1
        t_end = time.time()
        print(
            f"{counter}/{len(check_name_list)} usernames in the list already exists, \
            time consumed {t_end - t_start:.4f} seconds"
        )


def run_bloom_filter(dataset):
    print("Running demo of Bloom Filter...")

    # Build the data structure from text file
    build_bloom_filter_from_file(resamble_filename(SORTED_USERNAMES_FILE, dataset))

    # Load save binary data structure into memory
    bf = load_filter_from_disk(resamble_filename(SAVED_BLOOM_FILTER, dataset))

    # Test the lookup operation and benchmark with time elapsed
    check_usernames(bf, USERNAMES_CHECK_FILE)


def run_cuckoo_filter(dataset, ai=False):
    print("Running demo of Cuckoo Filter...")

    # Build the data structure from text file
    build_cuckoo_filter_from_file(
        resamble_filename(SORTED_USERNAMES_FILE, dataset), use_ai=ai
    )

    # Load save binary data structure into memory
    cf = load_filter_from_disk(resamble_filename(SAVED_CUCKOO_FILTER, dataset, ai))

    # Test the lookup operation and benchmark with time elapsed
    check_usernames(cf, USERNAMES_CHECK_FILE)


# Load text file data into list of strings
def prepare_data_for_simple_search(dataset):
    name_list = None
    check_list = None
    print("Loading data from file...")
    with open(resamble_filename(SORTED_USERNAMES_FILE, dataset), "r") as f:
        name_list = [line.strip() for line in f]

    with open(USERNAMES_CHECK_FILE, "r") as f:
        check_list = [line.strip() for line in f]

    if name_list is None or check_list is None:
        print("Usernames load failed. Exit.")

    return name_list, check_list


# Count total number of lines in dataset
def num_line(filename):
    count = 0
    with open(filename, "r") as f:
        for _ in f:
            count += 1
    return count
