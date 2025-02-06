#
#  demo.py
#  Login Checker Program
#
#  Created by Pinjing Xu on 2/1/25.
#  Copyright © 2025 Pinjing (Alex) Xu. All rights reserved.
#

from src.helper import prepare_data_for_simple_search

from src.helper import run_bloom_filter
from src.helper import run_cuckoo_filter

from src.simple_algorithms import run_linear_search
from src.simple_algorithms import run_binary_search
from src.simple_algorithms import run_hash_table


def main():
    print("Initializing data...")
    # Load data for simple search methods
    scale = 1
    name_list, check_list = None, None  # prepare_data_for_simple_search(scale)

    print("Hey! I'm the Login Checker program. Which methods do you wanna try?")
    print(
        "a. 1b\tb. 500m\tc. 250m\td. 150m\te. 100m\nf. 50m\tg. 10m\th. 1m"
        + " \n1. Linear Search\
            \n2. Binary Search\
            \n3. Hash Map\
            \n4. Bloom Filter\
            \n5. Cuckoo Filter\
            \n6. 2 and 3\
            \n7. 4 and 5\
            \n999. exit"
    )

    while True:
        option = input(
            "\nEnter a operation(number + letter, e.g. '2e' for binary search on 100m dataset): "
        )
        cmds = list(option)
        if option != "999" and len(cmds) != 2:
            print("Wrong input! Try again!")
            continue
        datasets = {
            "a": "_1b",
            "b": "_500m",
            "c": "_250m",
            "d": "_150m",
            "e": "_100m",
            "f": "_50m",
            "g": "_10m",
            "h": "_1m",
        }
        if option != 999 and cmds[1] not in datasets:
            print("Wrong dataset selection! Try again!")
            continue

        match cmds[0]:
            case "1":
                if name_list is None or check_list is None:
                    name_list, check_list = prepare_data_for_simple_search(
                        datasets[cmds[1]]
                    )

                run_linear_search(name_list, check_list)
            case "2":
                if name_list is None or check_list is None:
                    name_list, check_list = prepare_data_for_simple_search(
                        datasets[cmds[1]]
                    )

                run_binary_search(name_list, check_list)
            case "3":
                if name_list is None or check_list is None:
                    name_list, check_list = prepare_data_for_simple_search(
                        datasets[cmds[1]]
                    )

                run_hash_table(name_list, check_list)
            case "4":
                print("Clearing cache...")
                name_list = None
                check_list = None

                run_bloom_filter(datasets[cmds[1]])
            case "5":
                print("Clearing cache...")
                name_list = None
                check_list = None

                run_cuckoo_filter(datasets[cmds[1]])
            case "6":
                if name_list is None or check_list is None:
                    name_list, check_list = prepare_data_for_simple_search(
                        datasets[cmds[1]]
                    )

                run_binary_search(name_list, check_list)
                run_hash_table(name_list, check_list)
            case "7":
                print("Clearing cache...")
                name_list = None
                check_list = None

                run_bloom_filter(datasets[cmds[1]])
                run_cuckoo_filter(datasets[cmds[1]])
            case "999":
                print("Byebye~")
                return
            case _:
                print("Wrong input! Try again please.")


if __name__ == "__main__":
    main()
