import binascii
import hashlib
import os

from imohash import hashfile

def M(size):
    chunks = []
    hasher = hashlib.md5()
    while 16*len(chunks) < size:
        hasher.update(b'A')
        chunks.append(hasher.digest())

    return b''.join(chunks)[0:size]

def test_spec():
    tests = [
        (16384, 131072, 0,      "00000000000000000000000000000000"),
        (16384, 131072, 1,      "01659e2ec0f3c75bf39e43a41adb5d4f"),
        (16384, 131072, 127,    "7f47671cc79d4374404b807249f3166e"),
        (16384, 131072, 128,    "800183e5dbea2e5199ef7c8ea963a463"),
        (16384, 131072, 4095,   "ff1f770d90d3773949d89880efa17e60"),
        (16384, 131072, 4096,   "802048c26d66de432dbfc71afca6705d"),
        (16384, 131072, 131072, "8080085a3d3af2cb4b3a957811cdf370"),
        (16384, 131073, 131072, "808008282d3f3b53e1fd132cc51fcc1d"),
        (16384, 131072, 500000, "a0c21e44a0ba3bddee802a9d1c5332ca"),
        (50,    131072, 300000, "e0a712edd8815c606344aed13c44adcf")
        ]

    for test in tests:
        with open('.test_data', 'wb') as f:
            f.write(M(test[2]))
        assert binascii.hexlify(hashfile('.test_data', sample_threshhold=test[1], sample_size=test[0])) == test[3].encode()
        os.remove('.test_data')

