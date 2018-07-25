#!/bin/env/python2
import time

import cyruslib

# without SSL
try:
    imap = cyruslib.CYRUS("imap://localhost:143")
except cyruslib.CYRUSError:
    time.sleep(5)  # wait for cyrus to start
    imap = cyruslib.CYRUS("imap://localhost:143")
imap.login("cyrus", "cyrus")
imap.cm("user/test")
imap.sam("user/test", "test", "all")
imap.sam("user/test", "cyrus", "all")