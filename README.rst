imohash
=======

imohash is a fast, constant-time hashing library. It uses file
size and sampling to calculate hashes quickly, regardless of file size.
It was originally released as a `Go library <https://github.com/kalafut/imohash>`__.

``imosum`` is a sample application to hash files from the command line, similar to
md5sum.

Installation
------------

``pip install imohash``

Usage
-----

As a library:

.. code-block:: python

    from imohash import hashfile

    hashfile('foo.txt')
    'O\x9b\xbd\xd3[\x86\x9dE\x0e3LI\x83\r~\xa3'

    hashfile('foo.txt', hexdigest=True)
    'a608658926d8aa86b3db8208ad279bfe'

    # just hash the whole file if smaller then 200000 bytes. Default is 128K
    hashfile('foo.txt', sample_threshhold=200000)
    'x86\x9dE\x0e3LI\x83\r~\xa3O\x9b\xbd\xd3[E'

    # use samples of 1000 bytes. Default is 16K
    hashfile('foo.txt', sample_size=1000)
    'E\x0e3LI\x83\r~\xa3O\x9b\xbd\xd3[E\x23\x25'

    # hash an already opened file
    f = open('foo.txt', 'rb')
    hashfileobject(f)
    'O\x9b\xbd\xd3[\x86\x9dE\x0e3LI\x83\r~\xa3'

    # hash a file on a remote server
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.connect('host', username='username', password='verysecurepassword')
    ftp = ssh.open_sftp()
    hashfileobject(ftp.file('/path/to/remote/file/foo.txt'))
    'O\x9b\xbd\xd3[\x86\x9dE\x0e3LI\x83\r~\xa3'

Or from the command line:

``imosum *.jpg``

Uses
----

Because imohash only reads a small portion of a file's data, it is very
fast and well suited to file synchronization and deduplication,
especially over a fairly slow network. A need to manage media (photos
and video) over Wi-Fi between a NAS and multiple family computers is how
the library was born.

If you just need to check whether two files are the same, and understand
the limitations that sampling imposes (see below), imohash may be a good
fit.

Misuses
-------

Because imohash only reads a small portion of a file's data, it is not
suitable for:

-  file verification or integrity monitoring
-  cases where fixed-size files are manipulated
-  anything cryptographic

Design
------

(Note: a more precise description is provided in the `algorithm
description <https://github.com/kalafut/imohash/blob/master/algorithm.md>`__.)

imohash works by hashing small chunks of data from the beginning,
middle and end of a file. It also incorporates the file size into the
final 128-bit hash. This approach is based on a few assumptions which
will vary by application. First, file size alone *tends* (1) to be a
pretty good differentiator, especially as file size increases. And when
people do things to files (such as editing photos), size tends to
change. So size is used directly in the hash, and **any files that have
different sizes will have different hashes**.

Size is an effective differentiator but isn't sufficient. It can show
that two files aren't the same, but to increase confidence that
like-size files are the same, a few segments are hashed using
`murmur3 <https://en.wikipedia.org/wiki/MurmurHash>`__, a fast and
effective hashing algorithm. By default, 16K chunks from the beginning,
middle and end of the file are used. The ends of files often contain
metadata which is more prone to changing without affecting file size.
The middle is for good measure. The sample size can be changed for your
application.

1 Try ``du -a . | sort -nr | less`` on a sample of your files to check
this assertion.

Small file exemption
~~~~~~~~~~~~~~~~~~~~

Small files are more likely to collide on size than large ones. They're
also probably more likely to change in subtle ways that sampling will
miss (e.g. editing a large text file). For this reason, imohash will
simply hash the entire file if it is less than 128K. This parameter is
also configurable.

Performance
-----------

The standard hash performance metrics make no sense for imohash since
it's only reading a limited set of the data. That said, the real-world
performance is very good. If you are working with large files and/or a
slow network, expect huge speedups. (**spoiler**: reading 48K is quicker
than reading 500MB.)

Name
----

Inspired by `ILS marker
beacons <https://en.wikipedia.org/wiki/Marker_beacon>`__.

Credits
-------

-  The "sparseFingerprints" used in
   `TMSU <https://github.com/oniony/TMSU>`__ gave me some confidence in
   this approach to hashing.
-  Sébastien Paolacci's
   `murmur3 <https://github.com/spaolacci/murmur3>`__ library does all
   of the heavy lifting in the Go version.
-  As does Hajime Senuma's
   `mmh3 <https://github.com/hajimes/mmh3>`__ library for the Python version.
