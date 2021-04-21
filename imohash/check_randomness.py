#!/usr/bin/env python3
"""
Sometimes we need to use hex string to store files,
such as `e8/ac/e8ac086e6f025eb4e03430bb99ea10b0.jpg`,
or get files randomly by hex hash filename. So, the
hex hash string returned by hash function should be
random enough, especially for the first few letters.
"""
from imohash.imohash import hashfile
import os
from pprint import pprint

hash_and_files = dict()
char_count = {i: 0 for i in '0123456789abcdef'}

for home, dirs, files in os.walk('/usr/bin/'):
    for filename in files:
        path = os.path.join(home, filename)
        if not os.path.islink(path):  # ignore symbolic link
            hex_hash = hashfile(path, hexdigest=True)
            hash_and_files[hex_hash] = path
            char_count[hex_hash[:1]] += 1

hash_and_files = sorted(hash_and_files.items(), key=lambda x: x[0])

# print sorted hashes
for _hash, filename in hash_and_files:
    print(_hash, filename)

# print the number of the first char
pprint(char_count)
