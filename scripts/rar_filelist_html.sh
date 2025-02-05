#!/usr/bin/env bash
# print list of .html URLs from RAR containing website dump
if [ "$#" -ne 1 ] ; then
    echo "USAGE: $0 <website_dump_rar>"; exit 1
fi
unrar la "$1" | grep '\.html$' | rev | cut -d' ' -f1 | rev | sort
