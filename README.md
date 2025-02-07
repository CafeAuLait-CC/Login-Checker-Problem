# Login Checker Program - COSC 520 Assignment 1 

## Setup 

Go inside the project directory, then do the following to setup.
```
> python3 -m venv alg_assign
> source ./alg_assign/bin/activate
> pip install -r requirements.txt
```

### Dataset
Download the dataset from [Google Drive](https://drive.google.com/drive/folders/18dPf2WIguPIK68wyTIklPPpi2dBzVe3U?usp=sharing), and store everything under the `data/` and `data/prebuild` folder. 

To get started, let's just download an example and structure your folder as follows:
```
data/
    |
    |__ sorted_usernames_1m.txt
    |__ username_check_1m.txt
    |
    |__ prebuild/
          |
          |__ saved_bloom_filter_1m.pkl
          |__ saved_cuckoo_filter_1mAI.pkl
```

For details about the data file structure and usage, please check [here](data/README.md)


## Usage

```
> python demo.py
```
When the program starts, you will see an interactive menu looks like below:
```
Hey! I'm the Login Checker program. Which methods do you wanna try?
a. 1b	b. 500m	c. 250m	d. 150m	e. 100m	f. 50m	g. 10m	h. 1m
 
1. Linear Search            
2. Binary Search            
3. Hash Map            
4. Bloom Filter            
5. Cuckoo Filter            
6. 2 and 3            
7. 4 and 5            
999. exit

Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset):
```

Now you can type a combination of letter and digit to tell the program what you want to do. 

The `abcdefgh` indicate the dataset you want to use, and use the digits `1234567` or `999` to choose a algorithm(s) or exit the program.

Since you just downloaded the `1m` sets of data, you could start by typing `2h` and hit `Enter`. The program will start to run Binary Search on a "small" dataset.
```
Loading data from file...
Running demo of Binary Search...
Start searching...
100%|███████████████████████████████████████████████████████| 1000000/1000000 [00:02<00:00, 436872.54it/s]

Binary Search Done! 584/1000000 usernames in the list already exists,         time consumed 2.3124 seconds
Clearing cache...

Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset):
```

You will see the binary search finished in 2 seconds, and then the program will let you start a new round of testing.

The output information `584/1000000 usernames in the list already exists` means that out of the 1000000 usernames in `username_check_1m.txt`, 584 of them are found in the `sorted_usernames_1m.txt`.

We could also play with the Bloom Filter in this program. Without press Ctrl-C to terminate the program and restart it again, the program let you do multiple rounds after the previous run finishes. As shown in the last line of the previous output:
```
Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset):
```
If you have forgotten the letter+number combinations, just type a random word like `help`, and the program will show you the instructions again:
```
Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset): help

a. 1b	b. 500m	c. 250m	d. 150m	e. 100m	f. 50m	g. 10m	h. 1m
 
1. Linear Search            
2. Binary Search            
3. Hash Map            
4. Bloom Filter            
5. Cuckoo Filter            
6. 2 and 3            
7. 4 and 5            
999. exit

Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset):
```
Now, try `4h` to run Bloom Filter on this dataset.
```
Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset): 4h
Clearing cache...
Running demo of Bloom Filter...
Initializing...
Building Bloom Filter from file data/sorted_usernames_1m.txt
100%|███████████████████████████████████████████████████████| 1177822/1177822 [00:00<00:00, 1291067.57it/s]
Saving binary into  data/prebuild/saved_bloom_filter_1m.pkl
- Loading data from data/prebuild/saved_bloom_filter_1m.pkl
- Looking for usernames in filter
590/1000000 usernames in the list already exists,             time consumed 0.7833 seconds

Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset): 
```
Again, from the output, we can know that the algorithm first spend some time constructing a bloom filter from the text file `data/sorted_usernames_1m.txt`, then created a binary file called `data/prebuild/saved_bloom_filter_1m.pkl` storing the well constructed bloom filter for future use. After that, a search request is initiated. 1000000 search operations finished in 0.7833 seconds, and 590 of the usernames is found in the `data/sorted_usernames_1m.txt file.

You may have noticed that the 590 is a bit higher than the one we got after running the binary search, which was 584. This is because bloom filer is a probabilistic data structure, and there may be false positives in the results. It's a normal action, so no need to be panic!

Type `999` to exit the program
```
Enter a operation(number + letter, e.g. '2e' for binary search on 100Million (number of records) dataset): 999
Byebye!
```

#### More Funs

You have done a lot today! But the program can to a lot more!
Before you continue, remember to check the data file structure [here](data/README.md), and download the rest of the dataset according to your demand.

### Unit Test

Use the following command to run the unit test:
```
> python -m unittest
```
## Acknowledgement

A little part of the project source code are written by generative AI ([DeepSeek-V3](https://www.deepseek.com)), including the following files:
```
src/cuckoo_filter_ai.py
tests/test_bloom_filter.py
tests/test_cuckoo_filter.py
```


