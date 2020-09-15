py-wetransfer
=============

Python script for downloading wetransfer files (https://www.wetransfer.com/) in command line mode

Usage
=====

You should have a we transfer address similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ

So execute:

    python wetransfer.py -u https://www.wetransfer.com/downloads/XXXXXXXXXXXXXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY/ZZZZZ

And download it! :)

Requirements
=============

python

requests

    pip install requests


September 2020 notes
====================

I have updated this script to work with the latest WeTransfer links (as of mid-September 2020).  Many thanks to Alejandro Alonso and Marcos Besteiro López for starting this off.

It's not my first Python script, but I don't really know Python very well, so be gentle with me...

I have tested it on Windows 10 with Python 2.x and 3.x, and also on Linux (Raspberry Pi) with Python 2.x
