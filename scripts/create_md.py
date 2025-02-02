#! /usr/bin/env python3
from os.path import isdir, isfile
from sys import argv
def clean(s):
    s = s.strip()
    for k, v in [('﹖','?')]:
        s = s.replace(k,v)
    return s
assert len(argv) == 3, "USAGE: %s <input_url_txt> <output_url_md>"
assert isfile(argv[1]), "Input file not found: %s" % argv[1]
assert not (isfile(argv[2]) or isdir(argv[2])), "Output exists: %s" % argv[2]
f_in = open(argv[1], 'rt'); f_out = open(argv[2], 'wt')
for l in f_in:
    url = clean(l)
    f_out.write('* [%s](%s)\n' % (url, url))
f_in.close(); f_out.close()
