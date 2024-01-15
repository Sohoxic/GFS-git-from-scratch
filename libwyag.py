import argparse           # Git is a CLI application, so we’ll need something to parse command-line arguments
import collections        # We’ll need a few more container types than the base lib provides, most notably an OrderedDict
import configparser       # Git uses a configuration file format that is basically Microsoft’s INI format. The configparser module can read and write these files.
from datetime import datetime
import grp, pwd           # We’ll need, just once, to read the users/group database on Unix (grp is for groups, pwd for users). This is because git saves the numerical owner/group ID of files, and we’ll want to display that nicely (as text)
import fnmatch            # To support .gitignore, we’ll need to match filenames against patterns like *.txt. Filename matching is in… fnmatch
import hashlib            # Git uses the SHA-1 function quite extensively. In Python, it’s in hashlib.
from math import ceil
import os                 # os and os.path provide some nice filesystem abstraction routines
import re                 # for regular expressions
import sys                # We also need sys to access the actual command-line arguments (in sys.argv)
import zlib               # Git compresses everything using zlib. Python has that, too

