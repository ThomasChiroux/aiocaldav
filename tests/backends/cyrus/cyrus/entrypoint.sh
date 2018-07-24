#!/bin/sh
/initdirs
/etc/init.d/saslauthd start
/etc/init.d/rsyslog start

echo 'test' | saslpasswd2 -p -c test
echo 'cyrus' | saslpasswd2 -p -c cyrus

/usr/cyrus/libexec/master &
cd /srv/python-cyrus.git/source/ && python2 create_mailbox.py

touch /tmp/infinite.txt
tail -f /tmp/infinite.txt
