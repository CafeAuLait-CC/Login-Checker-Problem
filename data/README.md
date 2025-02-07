# Datasets

Please download the dataset from [Google Drive](https://drive.google.com/drive/folders/18dPf2WIguPIK68wyTIklPPpi2dBzVe3U?usp=sharing), and store everything under the `data/` and `data/prebuild` folder, with the similiar folder structure shown as below. 

```
data/
    |
    |__ sorted_usernames_1m.txt
    |__ ...
    |__ username_check_1m.txt
    |
    |__ prebuild/
          |
          |__ saved_bloom_filter_1m.pkl
          |__ ...
          |__ saved_cuckoo_filter_1mAI.pkl
          |__ ...
```


You can find the following files in the Drive folder:
```
data/sorted_usernames_1b.txt
data/sorted_usernames_500m.txt
data/sorted_usernames_250m.txt
data/sorted_usernames_150m.txt
data/sorted_usernames_100m.txt
data/sorted_usernames_50m.txt
data/sorted_usernames_10m.txt
data/sorted_usernames_1m.txt

data/username_check_1m.txt
```
#### Database Set

The above files are the datasets. Files start with `sorted_usernames` are text files that each line has an username(string) containing only lowercase letters and underscore `_`. 

The `_500m` or `_1b` notation in the filename indicate the amount of lines in that file, all usernames are sorted. For instance, `sorted_usernames_500m.txt` containing 500 million sorted lines of usernames, and `sorted_usernames_1b.txt` has 1 billion sorted usernames in it.

#### Insert Target Set
The `username_check_1m.txt` file contains 1 million unsorted usernames, for testing purpose. When you have an algorithm ready, you can take names in the `username_check_1m.txt` file, and look for them in the `sorted_usernames_Xm.txt` file, to benchmark your search algorithms.

### Pre-built Data Structure (Optional)

```
prebuild/saved_bloom_filter_1m.pkl
prebuild/saved_bloom_filter_10m.pkl
prebuild/saved_bloom_filter_50m.pkl
prebuild/saved_bloom_filter_100m.pkl
prebuild/saved_bloom_filter_150m.pkl
prebuild/saved_bloom_filter_250m.pkl
prebuild/saved_bloom_filter_500m.pkl
prebuild/saved_bloom_filter_1b.pkl

prebuild/saved_cuckoo_filter_1mAI.pkl
prebuild/saved_cuckoo_filter_10mAI.pkl
prebuild/saved_cuckoo_filter_50mAI.pkl
prebuild/saved_cuckoo_filter_100mAI.pkl
prebuild/saved_cuckoo_filter_150mAI.pkl
prebuild/saved_cuckoo_filter_250mAI.pkl
prebuild/saved_cuckoo_filter_500mAI.pkl
prebuild/saved_cuckoo_filter_1bAI.pkl
```

These files are prebuilt binary files. Due to the huge amount of data, building data structures from scratch like bloom filter and cuckoo filter is a time consuming task. Thus, I provide these binary files for users to load them directly into memory. 

To use these files, do the following in the code:
```
import pickle

from src.bloom_filter import BloomFilter
from src.cuckoo_filter import CuckooFilter

with open("prebuild/saved_bloom_filter_1m.pkl", 'rb') as f:
    bf = pickle.load(f)
    if bf.exist("alex"):
        print("Hi!")

with open("prebuild/saved_cuckoo_filter_1mAI.pkl", 'rb') as f:
    cf = pickle.load(f)
    if cf.exist("alex"):
        print("Hi!")
```
