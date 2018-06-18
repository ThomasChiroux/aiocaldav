#!/bin/sh
if [ "$1" = 'radicale' -a "$(id -u)" = '0' ]; then
    chown -R radicale .
    exec su-exec radicale "$@"
fi