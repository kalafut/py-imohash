#!/usr/bin/env python
from __future__ import division

import binascii
import glob
import os
import sys

import mmh3
import varint

SAMPLE_THRESHOLD = 128 * 1024
SAMPLE_SIZE = 16 * 1024


# Hashes an opened file object. Compatible with paramimo SFTPFile and regular files.
def hashfileobject(
    f, sample_threshold=SAMPLE_THRESHOLD, sample_size=SAMPLE_SIZE, hexdigest=False
):
    # get file size from file object
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0, os.SEEK_SET)

    if size < sample_threshold or sample_size < 1 or size < (4 * sample_size):
        data = f.read()
    else:
        data = read_full(f, sample_size)
        f.seek(size // 2)
        data += read_full(f, sample_size)
        f.seek(-sample_size, os.SEEK_END)
        data += read_full(f, sample_size)

    hash_tmp = mmh3.hash_bytes(data)
    hash_ = hash_tmp[7::-1] + hash_tmp[16:7:-1]
    enc_size = varint.encode(size)
    digest = enc_size + hash_[len(enc_size) :]

    return binascii.hexlify(digest).decode() if hexdigest else digest


# Reads exactly sample_size bytes from file object f, erroring if EOF is reached before that.
def read_full(f, sample_size):
    data = b""
    while len(data) < sample_size:
        chunk = f.read(sample_size - len(data))
        if not chunk:
            raise EOFError("Could not read enough data")
        if len(chunk) == sample_size:
            return chunk
        data += chunk
    return data


def hashfile(
    filename,
    sample_threshold=SAMPLE_THRESHOLD,
    sample_size=SAMPLE_SIZE,
    hexdigest=False,
):
    with open(filename, "rb") as f:
        return hashfileobject(f, sample_threshold, sample_size, hexdigest)


def imosum():
    if len(sys.argv) == 1:
        print("imosum filenames")
        return

    for fn in sys.argv[1:]:
        if not os.path.exists(fn):
            print("imosum: {}: No such file or directory".format(fn))
            continue
        if not os.path.isdir(fn):
            print("{}  {}".format(hashfile(fn, hexdigest=True), fn))
