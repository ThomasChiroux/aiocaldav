#!/bin/env/python2

import cyruslib

# without SSL
imap = cyruslib.CYRUS("imap://localhost:143")
imap.login("cyrus", "cyrus")
imap.cm("user/test")
imap.sam("user/test", "test", "all")
imap.sam("user/test", "cyrus", "all")